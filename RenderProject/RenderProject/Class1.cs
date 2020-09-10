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
            MessageBox.Show(myVegas.Version);
        }
    }
}

