from conans import ConanFile, CMake, tools
import os
import shutil


class PhysfsConan(ConanFile):
    name = "physfs"
    version = "3.0.1"
    description = "Provides abstract access to various archives"
    topics = ("conan", "physfs", "physicsfs", "archive")
    url = "https://github.com/bincrafters/conan-physfs"
    homepage = "https://icculus.org/physfs/"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "ZLIB"
    exports = "LICENSE.md"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        del self.settings.compiler.libcxx
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        folder = "{}-{}".format(self.name, self.version)
        tools.get("https://icculus.org/physfs/downloads/{}.tar.bz2".format(folder))
        os.rename(folder, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["PHYSFS_BUILD_TEST"] = False
        cmake.configure(build_folder=self._build_subfolder)
        cmake.build()

    def package(self):
        self.copy("LICENSE.txt", dst="licenses", src=self._source_subfolder)
        self.copy("physfs.h", dst="include", src=os.path.join(self._source_subfolder, "src"))
        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.lib", dst="lib", keep_path=False, excludes="*-static.lib")
            self.copy("*.so*", dst="lib", keep_path=False, symlinks=True)
            self.copy("*.dylib", dst="lib", keep_path=False, symlinks=True)
        else:
            self.copy("*-static.lib", dst="lib", keep_path=False)
            self.copy("*.a", dst="lib", keep_path=False, excludes="*.dll.a")
        self.copy("*.pdb", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags.extend(["-framework IOKit",
                                               "-framework Foundation"])
            self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        if self.settings.os == "Windows" and self.settings.compiler == "gcc":
            shutil.move(os.path.join(self.package_folder, "lib", "objects.a"), os.path.join(self.package_folder, "lib", "libobjects.a"))
