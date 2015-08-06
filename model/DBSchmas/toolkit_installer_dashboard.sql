CREATE TABLE IF NOT EXISTS [{product_name}_{year}_toolkit_installer_dashboard] (
  [installer_path] VARCHAR(200) NOT NULL, 
  [lv_version] VARCHAR(20) NOT NULL, 
  [lv_api_version] VARCHAR(20) NOT NULL, 
  [safemode] VARCHAR(20) NOT NULL, 
  [comment] text(1000), 
  CONSTRAINT [sqlite_autoindex_{product_name}_{year}_toolkit_installer_dashboard_1] PRIMARY KEY ([installer_path]));
