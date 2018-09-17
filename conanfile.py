from conans import ConanFile, CMake, tools
import os.path


class PhysfsConan(ConanFile):
    name = "physfs"
    version = "3.0.1"
    license = "zlib"
    url = "https://github.com/elizagamedev/conan-physfs"
    description = "Provides abstract access to various archives"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    sourcename = "{}-{}".format(name, version)

    def source(self):
        tools.get("https://icculus.org/physfs/downloads/{}.tar.bz2".format(self.sourcename))
        tools.replace_in_file(
            os.path.join(self.sourcename, "CMakeLists.txt"),
            "project(PhysicsFS)",
            """project(PhysicsFS)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=self.sourcename)
        cmake.build()

    def package(self):
        self.copy("physfs.h", dst="include", src=os.path.join(self.sourcename, "src"))
        if self.options.shared:
            self.copy("*.lib", dst="lib", keep_path=False, excludes="*-static.lib")
            self.copy("*.so", dst="lib", keep_path=False, symlinks=True)
            self.copy("*.dylib", dst="lib", keep_path=False, symlinks=True)
        else:
            self.copy("*-static.lib", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.pdb", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
