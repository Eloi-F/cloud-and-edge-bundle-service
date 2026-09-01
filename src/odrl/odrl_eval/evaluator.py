import os
import copy
import operator
import rdflib
from rdflib.collection import Collection
from rdflib.namespace import RDF
from dateutil import parser

import logging
from src.logging.logging_config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

ODRL = rdflib.Namespace("http://www.w3.org/ns/odrl/2/")

# --- OPERATEURS ODRL ---
OPS_MAP = {
    str(ODRL.eq): operator.eq,
    str(ODRL.neq): operator.ne,
    str(ODRL.lt): operator.lt,
    str(ODRL.lteq): operator.le,
    str(ODRL.gt): operator.gt,
    str(ODRL.gteq): operator.ge,
}

REFINEMENT_CONTEXTS = {
    str(ODRL.Party): ODRL.assignee,
    str(ODRL.Action): ODRL.action,
    str(ODRL.Asset): ODRL.target,
}


class ODRLEvaluator:
    def __init__(self, policies_dir="./policies"):
        """
        Initialise l'évaluateur et pré-charge toutes les politiques en mémoire.
        À appeler une seule fois au démarrage du programme.
        """
        self.master_policy = {}
        self._load_all_policies(policies_dir)

    def _load_all_policies(self, directory):
        if not os.path.isdir(directory):
            print(f"⚠️  Dossier {directory} introuvable.")
            return

        for filename in os.listdir(directory):
            if filename.endswith((".jsonld", ".ttl", ".rdf", ".xml")):
                filepath = os.path.join(directory, filename)
                self._load_policy_file(filepath)

        print(f"Resultat: {self.master_policy}")

    def _load_policy_file(self, filepath):
        graph = rdflib.Graph()
        try:
            graph.parse(
                filepath, format=rdflib.util.guess_format(filepath) or "json-ld"
            )
            parsed_policy = self._parse_policy(graph)

            policy_uid = parsed_policy.get("uid")
            if policy_uid:
                if policy_uid not in self.master_policy:
                    self.master_policy[policy_uid] = {
                        "permissions": [],
                        "prohibitions": [],
                        "obligations": [],
                    }

                self.master_policy[policy_uid]["permissions"].extend(
                    parsed_policy.get("permissions", [])
                )

                self.master_policy[policy_uid]["prohibitions"].extend(
                    parsed_policy.get("prohibitions", [])
                )

                self.master_policy[policy_uid]["obligations"].extend(
                    parsed_policy.get("obligations", [])
                )
            else:
                print(
                    f"⚠️ Aucune politique (Set, Request, etc.) trouvée dans {filepath}"
                )

        except Exception as e:
            print(f"❌ Erreur lecture de {filepath}: {e}")

    # ==========================================
    # LOGIQUE D'EXTRACTION DU GRAPHE
    # ==========================================
    def _extract_triplet(self, graph, node, prefix=None):
        lefts = list(graph.objects(node, ODRL.leftOperand))
        if lefts:
            op = list(graph.objects(node, ODRL.operator))
            right = list(graph.objects(node, ODRL.rightOperand))
            # left_str = f"{prefix} {lefts[0]}" if prefix else str(lefts[0])
            left_str = str(lefts[0])
            return [left_str, str(op[0]) if op else "", str(right[0]) if right else ""]

        for logic_op in [ODRL["and"], ODRL["or"], ODRL.xone, ODRL.andSequence]:
            for col_node in graph.objects(node, logic_op):
                try:
                    items = list(Collection(graph, col_node))
                    return [
                        str(logic_op),
                        [self._extract_triplet(graph, i, prefix) for i in items if i],
                    ]
                except Exception:
                    pass
        return None

    def _extract_rule_components(self, graph, rule_node):
        triplets = []
        for comp_type, predicate in REFINEMENT_CONTEXTS.items():
            for comp_node in graph.objects(rule_node, predicate):
                val = next(graph.objects(comp_node, RDF.value), comp_node)
                triplets.append([comp_type, str(ODRL.eq), str(val)])
                for ref in graph.objects(comp_node, ODRL.refinement):
                    # t = self._extract_triplet(graph, ref, prefix=comp_type)
                    t = self._extract_triplet(graph, ref)
                    if t:
                        triplets.append(t)

        for constraint in graph.objects(rule_node, ODRL.constraint):
            t = self._extract_triplet(graph, constraint)
            if t:
                triplets.append(t)

        return [
            list(x)
            for x in set(tuple(i) if isinstance(i, list) else i for i in triplets)
        ]

    def _parse_policy(self, graph):
        def build_struct(node):
            node_id = str(node)
            conditions = self._extract_rule_components(graph, node)

            if isinstance(node, rdflib.URIRef):
                conditions.append(
                    ["http://www.w3.org/ns/odrl/2/uid", str(ODRL.eq), node_id]
                )

            return {
                "uid": node_id,
                "conditions": conditions,
                "duties": [build_struct(d) for d in graph.objects(node, ODRL.duty)],
                "consequences": [
                    build_struct(c) for c in graph.objects(node, ODRL.consequence)
                ],
                "remedies": [build_struct(r) for r in graph.objects(node, ODRL.remedy)],
                "matches_count": 0,
                "required": 0,
            }

        policy = {"uid": None, "permissions": [], "prohibitions": [], "obligations": []}
        for p_type, key in [
            (ODRL.permission, "permissions"),
            (ODRL.prohibition, "prohibitions"),
            (ODRL.obligation, "obligations"),
        ]:
            for policy_node in graph.subjects(p_type):
                policy["uid"] = str(policy_node)
                for rule in graph.objects(policy_node, p_type):
                    policy[key].append(build_struct(rule))
        return policy

    # ==========================================
    # MOTEUR D'ÉVALUATION
    # ==========================================
    def _eval_constraint(self, log_entry, constraint):
        if isinstance(constraint, list) and isinstance(constraint[1], list):
            logic_op, subs = constraint[0], constraint[1]
            results = [self._eval_constraint(log_entry, sub) for sub in subs]
            if logic_op.endswith("and") or logic_op.endswith("andSequence"):
                return all(results)
            if logic_op.endswith("or"):
                return any(results)
            if logic_op.endswith("xone"):
                return sum(results) == 1
            return False

        left, op_symbol, right = constraint

        # Trouver la variable (gère les namespaces ex: vs http://example.com)
        # resolved_left = (
        #     left
        #     if left in log_entry
        #     else next((p for p in reversed(left.split()) if p in log_entry), None)
        # )
        # if not resolved_left or resolved_left not in log_entry:
        #     return False

        if left not in log_entry:
            return False
        resolved_left = left

        value = log_entry[resolved_left]
        if value is None or str(value).strip() == "":
            return False
        if op_symbol not in OPS_MAP:
            return False

        # Robustesse absolue pour les 'Actions' (gère les différences de namespace ODRL)
        if "Action" in resolved_left:
            val_str = str(value).split("/")[-1].split("#")[-1]
            right_str = str(right).split("/")[-1].split("#")[-1]
            return val_str == right_str

        # Dates
        if "dateTime" in resolved_left:
            try:
                return OPS_MAP[op_symbol](
                    parser.parse(str(value)).timestamp(),
                    parser.parse(str(right)).timestamp(),
                )
            except Exception:
                return False

        # Numérique vs String
        try:
            return OPS_MAP[op_symbol](float(value), float(right))
        except ValueError:
            return OPS_MAP[op_symbol](str(value), str(right))

    def _check_match(self, log_entry, rule):
        if all(self._eval_constraint(log_entry, c) for c in rule.get("conditions", [])):
            rule["matches_count"] += 1
            rule["required"] = 0
            return True
        return False

    def evaluate(self, bundle_id: str, metadata: dict | list):
        """
        Évalue un log ou un historique complet par rapport à la politique en mémoire.
        """
        if bundle_id not in self.master_policy:
            return {
                "is_valid": False,
                "missing_duties": [],
                "violations": [f"Aucune politique trouvée pour le bundle: {bundle_id}"],
            }

        policy = copy.deepcopy(self.master_policy[bundle_id])

        logs = metadata if isinstance(metadata, list) else [metadata]
        logs.sort(
            key=lambda x: parser.parse(
                x.get(str(ODRL.dateTime), "1970-01-01")
            ).timestamp()
        )

        validity = True
        violations = []

        # 2. Parcours de l'historique
        for log_entry in logs:
            matched_any_rule = False

            # Vérification des Permissions et de leurs Duties
            for p in policy["permissions"]:
                if self._check_match(log_entry, p):
                    matched_any_rule = True
                for d in p.get("duties", []):
                    if self._check_match(log_entry, d):
                        matched_any_rule = True

            # Vérification des Interdictions
            for pr in policy["prohibitions"]:
                if self._check_match(log_entry, pr):
                    matched_any_rule = True
                    violations.append(
                        f"Interdiction violée par l'action {log_entry.get(str(ODRL.Action))}"
                    )
                    validity = False

            # Si la ligne du log ne matche ni une permission, ni un duty = Action illégale !
            if not matched_any_rule and log_entry.get(str(ODRL.Action)):
                violations.append(
                    f"Action illégale ou contraintes non respectées : {log_entry[str(ODRL.Action)]}"
                )
                validity = False

        # 3. Vérification des Duties manquants à la FIN de l'historique
        missing_duties = []
        for p in policy["permissions"]:
            # Si on a utilisé cette permission au moins une fois
            if p["matches_count"] > 0:
                for d in p.get("duties", []):
                    # Mais qu'on n'a jamais fait le duty associé
                    if d["matches_count"] == 0:
                        d["required"] = 1
                        missing_duties.append(d)

        return {
            "is_valid": validity and len(violations) == 0,
            "missing_duties": missing_duties,
            "violations": violations,
        }
