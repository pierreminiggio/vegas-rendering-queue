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
            string filePath = "F:\\videos\\vlogs\\15 - Live API 3\\projet.veg";
            if (myVegas.OpenProject(filePath))
            {
                MessageBox.Show(filePath);
            }
            else
            {
                myVegas.Exit();
            }
        }
    }
}

