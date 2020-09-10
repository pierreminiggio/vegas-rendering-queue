using System;
using System.Collections.Generic;
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
            String inputFilePath = "F:\\videos\\vlogs\\15 - Live API 3\\projet.veg";
            if (myVegas.OpenProject(inputFilePath))
            {
                String rendererName = "Windows Media Video V11";
                String templateName = "Vidéo HD 1080-30p 8 Mbits/s";
                RenderArgs renderArgs = new RenderArgs(myVegas.Project);
                renderArgs.RenderTemplate = findTemplate(rendererName, templateName, myVegas.Renderers);
                String outputFilePath = "F:\\videos\\vlogs\\15 - Live API 3\\projet.veg";
                renderArgs.OutputFile = outputFilePath;
                RenderStatus renderStatus = myVegas.Render(renderArgs);
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

