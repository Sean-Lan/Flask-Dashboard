CREATE TABLE IF NOT EXISTS [{product_name}_{year}_bundle_installer_dashboard] (
  [bundle_path] VARCHAR(200) NOT NULL, 
  [lv_version] VARCHAR(20) NOT NULL, 
  [lv_api_version] VARCHAR(20) NOT NULL, 
  [safemode] VARCHAR(20) NOT NULL, 
  [toolkit_path] VARCHAR(200) NOT NULL, 
  [actual_size] VARCHAR(100) NOT NULL, 
  [dedupe_size] VARCHAR(100) NOT NULL, 
  [comment] TEXT(1000), 
  CONSTRAINT [sqlite_autoindex_{product_name}_{year}_bundle_installer_dashboard_1] PRIMARY KEY ([bundle_path]));
