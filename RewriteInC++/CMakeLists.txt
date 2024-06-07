cmake_minimum_required(VERSION 3.28)
project(1992Putnam)

# I tried using all kinds of packages to get the correct version of EVERYTHUNG, but none of them worked.
# anyway im keeping it for memory
set(CMAKE_CXX_STANDARD 17)

set(PYTHON_EXECUTABLE /opt/homebrew/bin/python3)

find_package(Eigen3 REQUIRED)
include_directories(${EIGEN3_INCLUDE_DIR})


find_package(Boost REQUIRED)

find_package(Python COMPONENTS Development REQUIRED)
include_directories(${Python_INCLUDE_DIRS})

find_package(CGAL REQUIRED)
include_directories(${CGAL_INCLUDE_DIRS})


set(MATPLOTLIB_CPP_DIR "/Users/dimitrichrysafis/CLionProjects/1992Putnam/matplotlib-cpp")
include_directories(${MATPLOTLIB_CPP_DIR})

set(NUMPY_INCLUDE_DIR /opt/homebrew/lib/python3.12/site-packages/numpy/core/include)

include_directories(${NUMPY_INCLUDE_DIR})

add_executable(1992Putnam main.cpp
        convex_hull.cpp
        convex_hull.h)


target_link_libraries(1992Putnam PRIVATE Eigen3::Eigen Boost::boost ${Python_LIBRARIES} ${CGAL_LIBRARIES})
