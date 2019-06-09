# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class GLBindingConan(ConanFile):
    name = "glbinding"
    version = "3.1.0"
    description = "glbinding leverages C++11 features like enum classes, lambdas, and variadic templates, \
                   instead of relying on macros; all OpenGL symbols are real functions and variables"

    topics = ("conan", "glbinding", "opengl")
    url = "https://github.com/bincrafters/conan-glbinding"
    homepage = "https://github.com/cginternals/glbinding"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False], 
        "fPIC": [True, False]
    }
    default_options = {
        "shared": False, 
        "fPIC": True
    }
    patches = [
        "0001-Fix-Windows-install-directories.patch"
    ]
    exports_sources = [] + patches

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/cginternals/glbinding"
        sha256 = "6729b260787108462ec6d8954f32a3f11f959ada7eebf1a2a33173b68762849e"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version),
                  sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)
        for patch_file in self.patches:
            self.output.info("Applying patch {}".format(patch_file))
            tools.patch(base_path=self._source_subfolder, patch_file=patch_file)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["OPTION_BUILD_EXAMPLES"] = False
        cmake.definitions["OPTION_BUILD_TOOLS"] = False
        cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE",
                  dst="licenses",
                  src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info(
            "Appending PATH environment variable: {}".format(bindir))
        self.env_info.PATH.append(bindir)
        self.cpp_info.libs = tools.collect_libs(self)
