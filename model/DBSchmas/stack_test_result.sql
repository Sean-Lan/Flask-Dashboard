CREATE TABLE IF NOT EXISTS [stack_test_result] (
  [daily_folder] VARCHAR(200) NOT NULL, 
  [validated_stack] VARCHAR(100) NOT NULL, 
  [os_name] VARCHAR(100) NOT NULL, 
  [target_name] VARCHAR(20) NOT NULL, 
  [pass_rate] FLOAT NOT NULL, 
  CONSTRAINT [] PRIMARY KEY ([daily_folder], [os_name], [target_name]));
