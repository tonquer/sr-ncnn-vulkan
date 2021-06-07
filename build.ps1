$LIB_NAME='waifu2x'
$TAG_NAME=(git describe --abbrev=0 --tags)
$HEAD_SHA_SHORT=(git rev-parse --short HEAD)
$PACKAGE_PREFIX=($LIB_NAME + '-' + $TAG_NAME + '_' + $HEAD_SHA_SHORT)
$PACKAGENAME=($PACKAGE_PREFIX + '-py39-windows')

# Vulkan SDK
Invoke-WebRequest -Uri `
  https://sdk.lunarg.com/sdk/download/1.2.162.0/windows/VulkanSDK-1.2.162.0-Installer.exe?Human=true `
  -OutFile VulkanSDK-1.2.162.0-Installer.exe
7z x -aoa .\VulkanSDK-1.2.162.0-Installer.exe -oVulkanSDK
Remove-Item .\VulkanSDK\Demos, `
            .\VulkanSDK\Samples, `
            .\VulkanSDK\Third-Party, `
            .\VulkanSDK\Tools, `
            .\VulkanSDK\Tools32, `
            .\VulkanSDK\Bin32, `
            .\VulkanSDK\Lib32 `
            -Recurse

# Python (x86_64)
$Env:VULKAN_SDK=((Get-Location).Path + '\VulkanSDK')
mkdir build; Set-Location .\build\
cmake -A x64 `
      -DNCNN_VULKAN=ON `
      -DNCNN_BUILD_TOOLS=OFF `
      -DNCNN_BUILD_EXAMPLES=OFF `
      -DPYTHON_EXECUTABLE="$($Env:pythonLocation + '\python.exe')" `
      -DPYBIND11_FINDPYTHON=OFF `
      -DPYBIND11_PYTHON_VERSION='3.9.5' `
      ..\src
Copy-Item -Verbose -Path "$($Env:pythonLocation + '\libs\python39.lib')" -Destination "$((Get-Location).Path)"
cmake --build . --config Release -j 2
Set-Location .\Release\
Move-Item waifu2x.dll waifu2x.pyd

# Package
Set-Location .\..\..\
mkdir "$(PACKAGENAME)"
Copy-Item -Verbose -Path "README.md" -Destination "$(PACKAGENAME)"
Copy-Item -Verbose -Path "LICENSE" -Destination "$(PACKAGENAME)"
Copy-Item -Verbose -Path "build\Release\waifu2x.pyd" -Destination "$(PACKAGENAME)"
Copy-Item -Verbose -Recurse -Path "models" -Destination "$(PACKAGENAME)"
Copy-Item -Verbose -Recurse -Path "test" -Destination "$(PACKAGENAME)"
