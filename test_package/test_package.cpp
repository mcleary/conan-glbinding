#include <glbinding/glbinding.h>

using GLProc = void(*)(void);

GLProc GetProcAddressStub(const char *) {
	return {};
}

int main() {
	glbinding::initialize(GetProcAddressStub, false);
}
