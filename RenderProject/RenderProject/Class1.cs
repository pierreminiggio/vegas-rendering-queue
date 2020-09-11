using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices.ComTypes;
using System.Text;
using System.Threading.Tasks;

//using System.Windows.Forms; -- Keep for debug via MessageBox.show(message)
using ScriptPortal.Vegas;

namespace RenderProject
{
    public class EntryPoint
    {
        public void FromVegas(Vegas myVegas)
        {
            string configString  = File.ReadAllText("./tmp.csv");
            string[] configArray = configString.Split(';');
            if (renderProject(myVegas, configArray[0], configArray[1], configArray[2], configArray[3]))
            {
                // Success
                myVegas.Exit();
            }
            else
            {
                // Failed
                myVegas.Exit();
            }
        }

        public bool renderProject(
            Vegas myVegas,
            string projectFilePath,
            string rendererName,
            string templateName,
            string outputFilePath
        )
        {
            if (myVegas.OpenProject(projectFilePath))
            {
                RenderArgs renderArgs = new RenderArgs(myVegas.Project);
                renderArgs.RenderTemplate = findTemplate(rendererName, templateName, myVegas.Renderers);
                renderArgs.OutputFile = outputFilePath;
                RenderStatus renderStatus = myVegas.Render(renderArgs);
                if (renderStatus == RenderStatus.Complete)
                {
                    return true;
                }
            }

            return false;
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

