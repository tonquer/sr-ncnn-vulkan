import setuptools, sys, os
from shutil import copyfile, copytree, rmtree
from setuptools.command.build_ext import build_ext
import subprocess
from distutils.core import Extension
import platform

long_description = \
"""
# waifu2x-ncnn-vulkan-python
- This is modified [waifu2x-ncnn-vulkan](https://github.com/nihui/waifu2x-ncnn-vulkan), Export pyd and so files to Python
- Support Linux, Windows, MacOs
- Support import JPG, PNG, BMP, GIF, WEBP, Animated WEBP, APNG
- Support export JPG, PNG, BMP, WEBP, Animated WEBP, APNG
- Support vulkan gpu and cpu

# Install
```shell
pip install waifu2x-vulkan
```

# Use
```shell
from waifu2x_vulkan import waifu2x_vulkan

# init
sts = waifu2x_vulkan.init()
print("init, code:{}".format(str(sts)))
isCpuModel = False
if sts < 0:
    # cpu model
    isCpuModel = True
    
gpuList = waifu2x_vulkan.getGpuInfo()
print(gpuList)
sts = waifu2x_vulkan.initSet(gpuId=0)
print("init set, code:{}".format(str(sts)))

# Model List:
#'MODEL_ANIME_STYLE_ART_RGB_NOISE0', 'MODEL_ANIME_STYLE_ART_RGB_NOISE0_TTA', 'MODEL_ANIME_STYLE_ART_RGB_NOISE1', 'MODEL_ANIME_STYLE_ART_RGB_NOISE1_TTA', 'MODEL_ANIME_STYLE_ART_RGB_NOISE2', 'MODEL_ANIME_STYLE_ART_RGB_NOISE2_TTA', 'MODEL_ANIME_STYLE_ART_RGB_NOISE3', 'MODEL_ANIME_STYLE_ART_RGB_NOISE3_TTA', 'MODEL_ANIME_STYLE_ART_RGB_NO_NOISE', 'MODEL_ANIME_STYLE_ART_RGB_NO_NOISE_TTA', 'MODEL_CUNET_NOISE0', 'MODEL_CUNET_NOISE0_TTA', 'MODEL_CUNET_NOISE1', 'MODEL_CUNET_NOISE1_TTA', 'MODEL_CUNET_NOISE2', 'MODEL_CUNET_NOISE2_TTA', 'MODEL_CUNET_NOISE3', 'MODEL_CUNET_NOISE3_TTA', 'MODEL_CUNET_NO_NOISE', 'MODEL_CUNET_NO_NOISE_TTA', 'MODEL_CUNET_NO_SCALE_NOISE0', 'MODEL_CUNET_NO_SCALE_NOISE0_TTA', 'MODEL_CUNET_NO_SCALE_NOISE1', 'MODEL_CUNET_NO_SCALE_NOISE1_TTA', 'MODEL_CUNET_NO_SCALE_NOISE2', 'MODEL_CUNET_NO_SCALE_NOISE2_TTA', 'MODEL_CUNET_NO_SCALE_NOISE3', 'MODEL_CUNET_NO_SCALE_NOISE3_TTA', 'MODEL_CUNET_NO_SCALE_NO_NOISE', 'MODEL_CUNET_NO_SCALE_NO_NOISE_TTA', 'MODEL_PHOTO_NOISE0', 'MODEL_PHOTO_NOISE0_TTA', 'MODEL_PHOTO_NOISE1', 'MODEL_PHOTO_NOISE1_TTA', 'MODEL_PHOTO_NOISE2', 'MODEL_PHOTO_NOISE2_TTA', 'MODEL_PHOTO_NOISE3', 'MODEL_PHOTO_NOISE3_TTA', 'MODEL_PHOTO_NO_NOISE', 'MODEL_PHOTO_NO_NOISE_TTA'

# add picture ...
# waifu2x.add(data=imgData, modelIndex=waifu2x_vulkan.MODEL_ANIME_STYLE_ART_RGB_NOISE0, backId=0, scale=2.5)
# waifu2x.add(data=imgData, modelIndex=waifu2x_vulkan.MODEL_ANIME_STYLE_ART_RGB_NOISE0, backId=0, format="webp", width=1000, high=1000)

# load picture...
# newData, format, backId, tick = waifu2x.load(0)
```

"""
Version = "1.1.6"

Plat = sys.platform

print(Plat)

build_temp = "build/temp/"
if Plat == "darwin":
    example_module = Extension('waifu2x_vulkan.waifu2x_vulkan',
    include_dirs=["build/temp/ncnntmp/src", "build/temp/pngtmp/", "build/temp/pngtmp/zlib", "src/ncnn/src", "src/libwebp/src",  "src/libpng", "src/libpng/zlib", "build/temp/src", "VulkanSDK/macos/include"],
    sources=['src/waifu2x_main.cpp', 'src/waifu2x_py.cpp', 'src/waifu2x.cpp'],
    extra_objects=[
        build_temp + "/ncnntmp/src/libncnn.a",
        build_temp + "/webptmp/libwebp.a",
        build_temp + "/webptmp/libwebpmux.a",
        build_temp + "/webptmp/libwebpdemux.a",
        build_temp + "/pngtmp/libpng.a",
        build_temp + "/pngtmp/zlib/libz.a",
        "VulkanSDK/macos/libMoltenVK.a",
        build_temp + "/ncnntmp/glslang/SPIRV/libSPIRV.a",
        build_temp + "/ncnntmp/glslang/glslang/libglslang.a",
        build_temp + "/ncnntmp/glslang/glslang/libMachineIndependent.a",
        build_temp + "/ncnntmp/glslang/OGLCompilersDLL/libOGLCompiler.a",
        build_temp + "/ncnntmp/glslang/glslang/OSDependent/Unix/libOSDependent.a",
        build_temp + "/ncnntmp/glslang/glslang/libGenericCodeGen.a",
        "-framework", "Metal",
        "-framework", "QuartzCore",
        "-framework", "CoreGraphics",
        "-framework", "Cocoa",
        "-framework", "IOKit",
        "-framework", "IOSurface",
        "-framework", "Foundation",
        "-framework", "CoreFoundation",
    ],
    )
    models = [example_module]
elif Plat in ["win32", "win64"]:
    example_module = Extension('waifu2x_vulkan.waifu2x_vulkan',
    include_dirs=["build/temp/ncnntmp/src", "build/temp/pngtmp/", "build/temp/pngtmp/zlib", "src/ncnn/src", "src/libwebp/src", "src/libpng", "src/libpng/zlib", "build/temp/src", "VulkanSDK/Include"],
    sources=['src/waifu2x_main.cpp', 'src/waifu2x_py.cpp', 'src/waifu2x.cpp'],
    define_macros=[("WIN32",1), ("NOMINMAX",1), ("NDEBUG",1)],
    extra_objects=[
        build_temp + "/ncnntmp/src/Release/ncnn.lib",
        build_temp + "/webptmp/Release/webp.lib",
        build_temp + "/webptmp/Release/webpmux.lib",
        build_temp + "/webptmp/Release/webpdemux.lib",
        build_temp + "/pngtmp/Release/libpng16_static.lib",
        build_temp + "/pngtmp/zlib/Release/zlibstatic.lib",
        "VulkanSDK/windows/vulkan-1.lib",
        build_temp + "/ncnntmp/glslang/SPIRV/Release/SPIRV.lib",
        build_temp + "/ncnntmp/glslang/glslang/Release/glslang.lib",
        build_temp + "/ncnntmp/glslang/glslang/Release/MachineIndependent.lib",
        build_temp + "/ncnntmp/glslang/OGLCompilersDLL/Release/OGLCompiler.lib",
        build_temp + "/ncnntmp/glslang/glslang/OSDependent/Windows/Release/OSDependent.lib",
        build_temp + "/ncnntmp/glslang/glslang/Release/GenericCodeGen.lib",
    ],
    )
    models = [example_module]
else:
    # linux
    if 'arm64' in platform.platform() or 'aarch64' in platform.platform():
        os.rename('VulkanSDK/linux/libvulkan.so', 'VulkanSDK/linux/libvulkan.x86.so')
        os.rename('VulkanSDK/linux/libvulkan.aarch64.so', 'VulkanSDK/linux/libvulkan.so')
    example_module = Extension('waifu2x_vulkan.waifu2x_vulkan',
    include_dirs=["build/temp/ncnntmp/src", "build/temp/pngtmp/", "build/temp/pngtmp/zlib", "src/ncnn/src", "src/libwebp/src",  "src/libpng", "src/libpng/zlib", "build/temp/src", "VulkanSDK/Include"],
    sources=['src/waifu2x_main.cpp', 'src/waifu2x_py.cpp', 'src/waifu2x.cpp'],
    extra_objects=[
        build_temp + "/ncnntmp/src/libncnn.a",
        build_temp + "/webptmp/libwebp.a",
        build_temp + "/webptmp/libwebpmux.a",
        build_temp + "/webptmp/libwebpdemux.a",
        build_temp + "/pngtmp/libpng.a",
        build_temp + "/pngtmp/zlib/libz.a",
        "VulkanSDK/linux/libvulkan.so",
        build_temp + "/ncnntmp/glslang/SPIRV/libSPIRV.a",
        build_temp + "/ncnntmp/glslang/glslang/libglslang.a",
        build_temp + "/ncnntmp/glslang/glslang/libMachineIndependent.a",
        build_temp + "/ncnntmp/glslang/OGLCompilersDLL/libOGLCompiler.a",
        build_temp + "/ncnntmp/glslang/glslang/OSDependent/Unix/libOSDependent.a",
        build_temp + "/ncnntmp/glslang/glslang/libGenericCodeGen.a",
        
    ],
    libraries=["gomp"],
    extra_compile_args=["-fopenmp"],
    extra_link_args=["-fopenmp"],

    )
    models = [example_module]

PLAT_TO_CMAKE = {
    "win32": "Win32",
    "win-amd64": "x64",
    "win-arm32": "ARM",
    "win-arm64": "ARM64",
}

class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        extdir = os.path.join(extdir, "ncnn")

        # required for auto-detection of auxiliary "native" libs
        if not extdir.endswith(os.path.sep):
            extdir += os.path.sep

        cfg = "Debug" if self.debug else "Release"

        # CMake lets you override the generator - we need to check this.
        # Can be set with Conda-Build, for example.
        cmake_generator = os.environ.get("CMAKE_GENERATOR", "")

        # Set Python_EXECUTABLE instead if you use PYBIND11_FINDPYTHON
        # EXAMPLE_VERSION_INFO shows you how to pass a value into the C++ code
        # from Python.
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}".format(extdir),
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE={}".format(extdir),
            "-DCMAKE_BUILD_TYPE={}".format(cfg),  # not used on MSVC, but no harm
            "-DNCNN_VULKAN=ON",
            "-DNCNN_BUILD_BENCHMARK=OFF",
            "-DNCNN_BUILD_EXAMPLES=OFF",
            "-DNCNN_BUILD_TOOLS=OFF",
        ]
        build_args = []

        if self.compiler.compiler_type != "msvc":
            # Using Ninja-build since it a) is available as a wheel and b)
            # multithreads automatically. MSVC would require all variables be
            # exported for Ninja to pick it up, which is a little tricky to do.
            # Users can override the generator with CMAKE_GENERATOR in CMake
            # 3.15+.
            pass
            # if not cmake_generator:
                # cmake_args += ["-GNinja"]
        else:
            # Single config generators are handled "normally"
            single_config = any(x in cmake_generator for x in {"NMake", "Ninja"})

            # CMake allows an arch-in-generator style for backward compatibility
            contains_arch = any(x in cmake_generator for x in {"ARM", "Win64"})

            # Specify the arch if using MSVC generator, but only if it doesn't
            # contain a backward-compatibility arch spec already in the
            # generator name.
            if not single_config and not contains_arch:
                cmake_args += ["-A", PLAT_TO_CMAKE[self.plat_name]]

            # Multi-config generators have a different way to specify configs
            if not single_config:
                cmake_args += [
                    "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir)
                ]
                build_args += ["--config", cfg]

        # Set CMAKE_BUILD_PARALLEL_LEVEL to control the parallel build level
        # across all generators.
        if "CMAKE_BUILD_PARALLEL_LEVEL" not in os.environ:
            # self.parallel is a Python 3 only way to set parallel jobs by hand
            # using -j in the build_ext call, not supported by pip or PyPA-build.
            if hasattr(self, "parallel") and self.parallel:
                # CMake 3.12+ only.
                build_args += ["-j{}".format(self.parallel)]

        ncnn_build_temp = build_temp + "ncnntmp/"
        webp_build_temp = build_temp + "webptmp/"
        png_build_temp = build_temp + "pngtmp/"
        if not os.path.exists(ncnn_build_temp):
            os.makedirs(ncnn_build_temp)
        if not os.path.exists(webp_build_temp):
            os.makedirs(webp_build_temp)
        if not os.path.exists(png_build_temp):
            os.makedirs(png_build_temp)

        # build libpng
        png_args = [
            "-DPNG_STATIC=ON",
            "-DPNG_SHARED=OFF",
            "-DPNG_TESTS=OFF",
            "-DPNG_EXECUTABLES=OFF",
        ]
        subprocess.check_call(
            ["cmake", os.path.abspath("src/libpng")] + png_args, cwd=png_build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=png_build_temp
        )

        # build webp
        webp_args = [
            "-DWEBP_ENABLE_SIMD=ON",
            "-DWEBP_BUILD_ANIM_UTILS=OFF",
            "-DWEBP_BUILD_CWEBP=OFF",
            "-DWEBP_BUILD_DWEBP=OFF",
            "-DWEBP_BUILD_GIF2WEBP=OFF",
            "-DWEBP_BUILD_IMG2WEBP=OFF",
            "-DWEBP_BUILD_VWEBP=OFF",
            "-DWEBP_BUILD_WEBPINFO=OFF",
            "-DWEBP_BUILD_WEBPMUX=OFF",
            "-DWEBP_BUILD_EXTRAS=OFF",
            "-DWEBP_BUILD_WEBP_JS=OFF",
            "-DWEBP_NEAR_LOSSLESS=OFF",
            "-DWEBP_ENABLE_SWAP_16BIT_CSP=OFF",
        ]
        subprocess.check_call(
            ["cmake", os.path.abspath("src/libwebp")] + webp_args, cwd=webp_build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=webp_build_temp
        )

        # build ncnn
        if Plat == "darwin":
            if "86" not in platform.machine():
                cmake_args += [
                    "-DCMAKE_OSX_ARCHITECTURES=x86_64;arm64",
                ]
            cmake_args += [
                "-DOpenMP_C_FLAGS=\"-Xclang -fopenmp\"",
                "-DOpenMP_CXX_FLAGS=\"-Xclang -fopenmp\"",
                "-DOpenMP_C_LIB_NAMES=libomp",
                "-DOpenMP_CXX_LIB_NAMES=libomp",
                "-DOpenMP_libomp_LIBRARY={}".format(os.path.abspath("VulkanSDK/macos/libomp.a")),
                "-DVulkan_LIBRARY={}".format(os.path.abspath("VulkanSDK/macos")),
                "-DVulkan_INCLUDE_DIR={}".format(os.path.abspath("VulkanSDK/macos/include")),
            ]
        elif Plat in ["win32", "win64"]:
            cmake_args += [
                "-DVulkan_LIBRARY={}".format(os.path.abspath("VulkanSDK/windows")),
                "-DVulkan_INCLUDE_DIR={}".format(os.path.abspath("VulkanSDK/Include")),
            ]
        else:
            cmake_args += [
                "-DVulkan_LIBRARY={}".format(os.path.abspath("VulkanSDK/linux/")),
                "-DVulkan_INCLUDE_DIR={}".format(os.path.abspath("VulkanSDK/Include")),
            ]
        subprocess.check_call(
            ["cmake", os.path.abspath("src/ncnn")] + cmake_args, cwd=ncnn_build_temp
        )
        subprocess.check_call(
            ["cmake", "--build", "."] + build_args, cwd=ncnn_build_temp
        )

        self.force = True
        return super(self.__class__, self).build_extension(ext)

setuptools.setup(
    name="waifu2x-vulkan",
    version=Version,
    author="tonquer",
    license="MIT",
    author_email="tonquer@qq.com",
    description="A waifu2x python tool, use nihui/waifu2x-ncnn-vulkan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonquer/waifu2x-vulkan",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: MIT License",
    ],
    python_requires = ">=3.6",
    include_package_data=True,
    entry_points={
        "pyinstaller40": [
            "hook-dirs = waifu2x_vulkan:get_hook_dirs"
        ]
    },
    cmdclass={"build_ext": CMakeBuild},
    ext_modules=models,
)

# python setup.py sdist
