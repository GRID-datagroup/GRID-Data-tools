# Version of the GRID Data Tools
__version__ = "0.1.0a0"

import os
import pathlib

package_dir = str(pathlib.Path(__file__).parent.absolute())
data_path = os.path.join(package_dir, "data")
