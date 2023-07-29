# Third Strike AI

Original docs can be found here: https://github.com/finalburnneo/FBNeo

## Setup

1. Build the macOS project

```bash
xcodebuild -project ./projectfiles/xcode/Emulator.xcodeproj -scheme Emulator -derivedDataPath ./.build
```

2. Install the package in a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install ai/
```

3. Run

```bash
third-strike-ai './.build/Build/Products/Debug/FinalBurn Neo.app/Contents/MacOS/FinalBurn Neo'
```
