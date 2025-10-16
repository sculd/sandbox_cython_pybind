#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

double sum_array(py::array_t<double> arr) {
    auto r = arr.unchecked<1>();  // 1D view
    double s = 0;
    for (ssize_t i = 0; i < r.shape(0); i++) {
        s += r(i);
    }
    return s;
}

PYBIND11_MODULE(bench_cpp, m) {
    m.def("sum_array", &sum_array, "Sum elements of numpy array");
}
