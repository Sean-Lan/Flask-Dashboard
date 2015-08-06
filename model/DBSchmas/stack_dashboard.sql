CREATE TABLE IF NOT EXISTS [myrio_roborio_{year}_stack_dashboard] (
  [validated_stack] VARCHAR(100) NOT NULL, 
  [validated_stack_url] VARCHAR(200) NOT NULL, 
  [lv_version] VARCHAR(20) NOT NULL, 
  [lv_api_version] VARCHAR(20) NOT NULL, 
  [safemode] VARCHAR(20) NOT NULL, 
  [comment] TEXT(1000), 
  CONSTRAINT [sqlite_autoindex_myrio_roborio_{year}_stack_dashboard_1] PRIMARY KEY ([validated_stack]));
