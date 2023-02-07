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
            ServiceName = "SpotifyKeyboard";
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
                if (!process.HasExited)
                {
                    process.Kill();
                }
            }
            catch (Exception ex)
            {
                // Handle the exception here
            }
        }
    }
}
