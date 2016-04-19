from ipykernel.kernelapp import IPKernelApp
from .kernel import GaucheKernel

IPKernelApp.launch_instance(kernel_class=GaucheKernel)
