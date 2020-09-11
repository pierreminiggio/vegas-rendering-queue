using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices.ComTypes;
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

            string configString  = File.ReadAllText("./tmp.csv");
            string[] configArray = configString.Split(';');
            string inputFilePath = configArray[0];
            string rendererName = configArray[1];
            string templateName = configArray[2];
            string outputFilePath = configArray[3];

            if (myVegas.OpenProject(inputFilePath))
            {
                RenderArgs renderArgs = new RenderArgs(myVegas.Project);
                renderArgs.RenderTemplate = findTemplate(rendererName, templateName, myVegas.Renderers);
                renderArgs.OutputFile = outputFilePath;
                RenderStatus renderStatus = myVegas.Render(renderArgs);
                if (renderStatus == RenderStatus.Complete)
                {
                    // done
                    myVegas.Exit();
                } else
                {
                    // failed
                    myVegas.Exit();
                }
                
            }
            else
            {
                myVegas.Exit();
            }
        }

        public RenderTemplate findTemplate(String rendererName, String templateName, Renderers renderers)
        {
            foreach (Renderer renderer in renderers)
            {
                if (renderer.FileTypeName == rendererName)
                {
                    foreach (RenderTemplate template in renderer.Templates)
                    {
                        if (template.Name == templateName)
                        {
                            return template;
                        }
                    }
                }
            }

            throw new Exception("Template not found");
        }
    }
}

