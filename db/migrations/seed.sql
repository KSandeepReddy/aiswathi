INSERT INTO topics (slug, name, description) VALUES
  ('physics', 'Physics', 'IIT JEE Physics'),
  ('physics/kinematics', 'Kinematics', 'Motion in one and two dimensions'),
  ('chemistry', 'Chemistry', 'IIT JEE Chemistry'),
  ('math', 'Mathematics', 'IIT JEE Mathematics');

INSERT INTO questions (topic_slug, text, options, answer_index, difficulty, tags) VALUES
  ('physics/kinematics', 'A body starts from rest and accelerates at 2 m/s^2. What is its velocity after 5 s?', '{"2 m/s","5 m/s","10 m/s","20 m/s"}', 2, 1400, '{kinematics,velocity}'),
  ('chemistry', 'What is the hybridization of carbon in methane?', '{"sp","sp2","sp3","sp3d"}', 2, 1300, '{bonding}'),
  ('math', 'Evaluate the derivative of sin(x).', '{"cos(x)","-cos(x)","sin(x)","-sin(x)"}', 0, 1200, '{calculus}');
