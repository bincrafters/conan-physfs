from conans import ConanFile, CMake, tools
import os


class PhysfsConan(ConanFile):
    name = "physfs"
    version = "stable-3.0"
    license = "ZLIB"
    url = "https://github.com/bincrafters/conan-physfs"
    homepage = "https://icculus.org/physfs/"
    author = "Bincrafters <bincrafters@gmail.com>"
    description = "Provides abstract access to various archives"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = "LICENSE.md"
    exports_sources = "CMakeLists.txt"

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def source(self):
        folder = "{}-{}".format(self.name, self.version)
        tools.get("https://hg.icculus.org/icculus/physfs/archive/{}.tar.bz2".format(self.version))
        os.rename(folder, self.source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()

    def package(self):
        self.copy("LICENSE.txt", dst="licenses", src=self.source_subfolder)
        self.copy("physfs.h", dst="include", src=os.path.join(self.source_subfolder, "src"))
        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.lib", dst="lib", keep_path=False, excludes="*-static.lib")
            self.copy("*.so*", dst="lib", keep_path=False, symlinks=True)
            self.copy("*.dylib", dst="lib", keep_path=False, symlinks=True)
        else:
            self.copy("*-static.lib", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
