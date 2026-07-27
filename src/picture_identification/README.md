## Environment Variables

| Variable              | Description                                      | Default                         |
| --------------------- | ------------------------------------------------ | ------------------------------- |
| `YOLO_MODEL_PATH`     | Path to the YOLO model used by the application.  | `./models/yolo26x.pt`           |
| `POLICIES_PATH`       | Path to the directory containing ODRL policies.  | `./policies`                    |
| `ORCHESTRATOR_DOMAIN` | The domain anycast used by orchestrators.        | `example_orchestrator.com`      |
| `PORT`                | Port on which the application listens.           | `8000`                          |
| `HOST_DOMAIN`         | Host domain or IP address of the service.        | `127.0.0.1`                     |
| `PROTOCOL`            | Protocol used to build the service base URL.     | `http`                          |
| `NODE_ID`             | Unique identifier of the service node.           | `System hostname`               |
