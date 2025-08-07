import uvicorn

host = "0.0.0.0"
port = 8108
reload = True
log_level = "info"


def main():
    """启动Rover Card服务"""
    print("🎴 启动Rover Card服务...")
    print(f"📱 访问 http://localhost:{port} 来使用Rover Card功能")
    uvicorn.run(
        "rovercard.core:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
    )


if __name__ == "__main__":
    main()
