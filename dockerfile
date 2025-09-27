FROM kivy/kivy:latest

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install buildozer in kivy environment
RUN pip install buildozer

# Install Android SDK
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    wget \
    unzip

# Download Android SDK
RUN wget -q https://dl.google.com/android/repository/commandlinetools-linux-8512546_latest.zip -O /tmp/sdk.zip \
    && mkdir -p /opt/android-sdk \
    && unzip -q /tmp/sdk.zip -d /opt/android-sdk \
    && mkdir -p /opt/android-sdk/cmdline-tools/latest \
    && mv /opt/android-sdk/cmdline-tools/* /opt/android-sdk/cmdline-tools/latest/ \
    && rm /tmp/sdk.zip

# Set environment variables
ENV ANDROID_SDK_ROOT=/opt/android-sdk
ENV PATH=$PATH:/opt/android-sdk/cmdline-tools/latest/bin

# Accept licenses
RUN yes | /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses

CMD ["buildozer", "android", "debug"]
