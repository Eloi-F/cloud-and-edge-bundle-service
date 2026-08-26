import sqlite3
from app.api.schemas import Detection


def connection():
	"""Return cursor object to handle database."""
	return sqlite3.connect("training.db")


def create_storage():
	"""Create database with all three tables."""
	try:
		with connection() as conn:
			conn.execute("PRAGMA foreign_keys = ON")
			cursor = conn.cursor()

			create = '''CREATE TABLE IF NOT EXISTS bounding_boxes (
					    id     INTEGER PRIMARY KEY AUTOINCREMENT,
					    x      INTEGER NOT NULL,
					    y      INTEGER NOT NULL,
					    width  INTEGER NOT NULL,
					    height INTEGER NOT NULL
					);

					CREATE TABLE IF NOT EXISTS detections (
					    id          INTEGER PRIMARY KEY AUTOINCREMENT,
					    classID     INTEGER NOT NULL,
					    conf        REAL,
					    boxID       INTEGER NOT NULL,
					    trainingID  INTEGER NOT NULL,
					    FOREIGN KEY (boxID) REFERENCES bounding_boxes(id),
					    FOREIGN KEY (trainingID) REFERENCES training(id)
					);
					
					CREATE TABLE IF NOT EXISTS training (
					    id      INTEGER PRIMARY KEY AUTOINCREMENT,
					    img     TEXT,
					    speed   REAL
					);'''

			cursor.executescript(create)
			conn.commit()

	except Exception as e:
		print("Error occurred while creating table BoundingBoxes : %s", e)


def store_sample(
		image: str,
		speed: float | None,
		detections: list[Detection]
) -> bool:
	"""Store sample in database."""
	try:
		with connection() as conn:
			cursor = conn.cursor()

			insert_box = '''INSERT INTO 
				bounding_boxes (x, y, width, height)
				VALUES (?, ?, ?, ?);'''

			insert_detection = '''INSERT INTO 
				detections (classID, conf, boxID, trainingID)
				VALUES (?, ?, ?, ?);'''

			insert_training = '''INSERT INTO
				training (img, speed)
				VALUES(?, ?);'''

			# Add image and speed in training table
			cursor.execute(insert_training, (image, speed))
			training_id = cursor.lastrowid

			# for each detection made in the image
			for detection in detections:
				# Add all object's boxes in bounding_boxes table
				cursor.execute(
					insert_box,
					(
						detection.box.x,
						detection.box.y,
						detection.box.width,
						detection.box.height,
					))
				box_id = cursor.lastrowid

				# Add detection in detection table
				cursor.execute(
					insert_detection,
					(
						detection.classId,
						detection.confidence,
						box_id,
						training_id
					)
				)
			conn.commit()
			return True

	except Exception as e:
		print("Error occurred while inserting sample: %s", e)
		return False
