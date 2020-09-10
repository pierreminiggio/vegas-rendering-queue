using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

using System.Windows.Forms;
using ScriptPortal.Vegas;

namespace RenderProject
{
    public class EntryPoint
    {
        public void FromVegas(Vegas myVegas)
        {
            string inputFilePath = "F:\\videos\\vlogs\\15 - Live API 3\\projet.veg";
            if (myVegas.OpenProject(inputFilePath))
            {
                RenderArgs renderArgs = new RenderArgs(myVegas.Project);
                //RenderTemplate renderTemplate = new RenderTemplate();
                //renderArgs.RenderTemplate = renderTemplate;
                renderArgs.ShowOpenButtonsOnComplete = false;
                renderArgs.SaveAsMono = false;
                string outputFilePath = "F:\\videos\\vlogs\\15 - Live API 3\\projet.veg";
                renderArgs.OutputFile = outputFilePath;
                //RenderStatus renderStatus = myVegas.Render(renderArgs);
            }
            else
            {
                myVegas.Exit();
            }
        }
    }
}

