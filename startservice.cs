using System;
using System.ServiceProcess;
using System.Diagnostics;
using System.IO;

namespace Spotify_automatization
{
    static class Program
    {
        static void Main()
        {
            ServiceBase[] ServicesToRun;
            ServicesToRun = new ServiceBase[] 
            { 
                new MyService() 
            };
            ServiceBase.Run(ServicesToRun);
        }
    }
}

namespace Spotify_automatization
{
    public partial class MyService : ServiceBase
    {
        private Process process;

        public MyService()
        {
            ServiceName = "FlowPlaylist";
        }

        protected override void OnStart(string[] args)
        {
            string exeFileName = "hid_control.exe";
            string servicePath = Path.GetDirectoryName(System.Reflection.Assembly.GetExecutingAssembly().Location);
            string exePath = Path.Combine(servicePath, exeFileName);

            process = new Process();
            process.StartInfo.FileName = exePath;
            process.StartInfo.WindowStyle = ProcessWindowStyle.Hidden;
            process.Start();
        }

        protected override void OnStop()
        {
            try
            {
                    var processes = Process.GetProcessesByName("hid_control");
            foreach (var process in processes)
            {
                process.Kill();
            }
            }
            catch (Exception ex)
            {
                File.WriteAllText("error.log", ex.Message);
            }
        }
    }
}
