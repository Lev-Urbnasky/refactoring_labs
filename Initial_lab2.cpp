void InstallDriver(string drive)
{
    string PathToODBCINI = Environment.GetEnvironmentVariable("windir",  EnvironmentVariableTarget.Machine) + @"\ODBC.INI";
    if (!File.Exists(PathToODBCINI))
    {
       try
       {
          File.Create(PathToODBCINI).Close();
       }
       catch (Exception e)
       {
          MessageBox.Show(e.Message);
       }
    }
    StreamReader sr = new StreamReader(PathToODBCINI,    System.Text.ASCIIEncoding.Default);
    string content = sr.ReadToEnd();
    sr.Close();
    int index = content.IndexOf("[ODBC Data Sources]");
    if (index >= 0)
    {
       int lastIndex = content.IndexOf("QEWSD=34751", index) + 11;
       try
       {
           content = content.Remove(index, lastIndex - index);
       }
       catch
       {
           MessageBox.Show(ERROR_WRONG_PREVIOUS_INSTALLATION);
       }
    };
    string path_to_driver = Helpers.AppExecFolder + "files\\driver.txt";
    if (File.Exists(path_to_driver))
    {
        sr = new StreamReader(path_to_driver);
        string driver_text = sr.ReadToEnd();
        driver_text = driver_text.Replace("{1}", drive);
        sr.Close();
        try
        {
            StreamWriter sw = new StreamWriter(File.OpenWrite(PathToODBCINI), System.Text.ASCIIEncoding.Default);
            string config = String.Format("{0}{1}", driver_text, content);
            sw.Write(config);
            sw.Close();
            MessageBox.Show("Installation completed");
        }
        catch
        {
            MessageBox.Show(e1.Message);
        }
     }
     else
     {
        MessageBox.Show(String.Format("Cannot find file {0}", path_to_driver));
     }
}
