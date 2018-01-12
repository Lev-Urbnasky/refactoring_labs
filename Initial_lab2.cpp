void CheckExistenceOrCreateODBC(string _name)
{
    if (!File.Exists(_name))
    {
        try
        {
            File.Create(_name).Close();
        }
        catch (Exception e)
        {
            throw;
        }
    }
}
 
string ReadContentsFromFile(string pathToFile)
{
    StreamReader sr = new StreamReader(pathToFile, System.Text.ASCIIEncoding.Default);
    string content = sr.ReadToEnd();
    sr.Close();
 
    return content;
}
 
void RemovePreviousInstallationInfo(string _content)
{
    int index = _content.IndexOf("[ODBC Data Sources]");
    if (index >= 0)
    {
        int lastIndex = _content.IndexOf("QEWSD=34751", index) + 11;
        try
        {
            _content = _content.Remove(index, lastIndex - index);
        }
        catch
        {
            MessageBox.Show(ERROR_WRONG_PREVIOUS_INSTALLATION);
        }
    };
}
 
void WriteDriverText(string _pathToDriver, string driver_text, string content)
{
    StreamWriter sw = new StreamWriter(File.OpenWrite(_pathToDriver), System.Text.ASCIIEncoding.Default);
    string config = String.Format("{0}{1}", driver_text, content);
    sw.Write(config);
    sw.Close();
}
 
void InstallDriver(string drive)
{
    string PathToODBCINI = Environment.GetEnvironmentVariable("windir", EnvironmentVariableTarget.Machine) + @"\ODBC.INI";
    try
    {
        CheckExistenceOrCreateODBC(PathToODBCINI);
    }
    catch (Exception e)
    {
        MessageBox.Show(e.Message);
        return;
    }
 
    string content = ReadContentsFromFile(PathToODBCINI);
    RemovePreviousInstallationInfo(content);
 
    string path_to_driver = Helpers.AppExecFolder + "files\\driver.txt";
    if (File.Exists(path_to_driver))
    {
        string driver_text = ReadContentsFromFile(path_to_driver);
        driver_text = driver_text.Replace("{1}", drive);
        try
        {
            WriteDriverText(PathToODBCINI, driver_text, content);
            MessageBox.Show("Installation completed");
        }
        catch (Exception e1)
        {
            MessageBox.Show(e1.Message);
        }
    }
    else
    {
        MessageBox.Show(String.Format("Cannot find file {0}", path_to_driver));
    }
}