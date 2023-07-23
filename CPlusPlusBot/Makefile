# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 -pthread
LIBS = -lcurl

# Directories
SRC_DIR = .
OBJ_DIR = obj
BIN_DIR = bin

# Source files (without json.hpp)
SOURCES = main.cpp \
          TradeManager/OandaManager.cpp \
          ExchangeCalls/APIcalls.cpp \
          DataCleaner/JSONhelpers.cpp

# Object files
OBJECTS = $(addprefix $(OBJ_DIR)/, $(SOURCES:.cpp=.o))

# Target executable
TARGET = $(BIN_DIR)/my_program

# Rule to build the executable
$(TARGET): $(OBJECTS)
	@mkdir -p $(BIN_DIR)
	$(CXX) $(CXXFLAGS) $(LIBS) $(OBJECTS) -o $(TARGET)

# Rule to create the necessary subdirectories and compile source files into object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(@D)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean rule to remove generated object files and the target executable
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

# Phony target to avoid conflicts with files named "clean" or "all"
.PHONY: clean all

# Default target (build the executable)
all: $(TARGET)

