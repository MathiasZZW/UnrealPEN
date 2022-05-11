// Fill out your copyright notice in the Description page of Project Settings.

#include "MyPen.h"
#include "Camera/CameraComponent.h"
#include <String>
#include "sockets.h"
#include"Networking.h"
#include <string>
#include <thread>
#include <vector>

DEFINE_LOG_CATEGORY_STATIC(PenLog, Log, All);
// Sets default values
AMyPen::AMyPen()
{
	//UE_LOG(PenLog, Warning, TEXT("Your First###################################"))
 	// Set this pawn to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	// 将该pawn设为由最小编号玩家控制
	AutoPossessPlayer = EAutoReceiveInput::Player0;
	// 创建可附加内容的虚拟根组件。
	RootComponent = CreateDefaultSubobject<USceneComponent>(TEXT("RootComponent"));
	// 创建相机和可见对象
	UCameraComponent* OurCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("OurCamera"));
	OurVisibleComponent = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("OurVisibleComponent"));
	// 将相机和可见对象附加到根组件。偏移并旋转相机。
	OurCamera->SetupAttachment(RootComponent);
	OurCamera->SetRelativeLocation(FVector(-250.0f, 0.0f, 250.0f));
	OurCamera->SetRelativeRotation(FRotator(-45.0f, 0.0f, 0.0f));
	OurVisibleComponent->SetupAttachment(RootComponent);
	
}
void AMyPen::Move_XAxis(float AxisValue)
{
	// 以100单位/秒的速度向前或向后移动
	CurrentVelocity.X = FMath::Clamp(AxisValue, -1.0f, 1.0f) * 200.0f;
}
void AMyPen::Move_YAxis(float AxisValue)
{
	//ScreenMsg("No sender socket");
	//UE_LOG(PenLog, Warning, TEXT("Your WWWWW %f"),AxisValue);
	// 以100单位/秒的速度向右或向左移动
	CurrentVelocity.Y = FMath::Clamp(AxisValue, -1.0f, 1.0f) * 100.0f;

}

bool AMyPen::GetButtonValue(bool but)
{
	if (but) { return Button1; }
	else { return Button0; }

}


// Called when the game starts or when spawned
void AMyPen::BeginPlay()
{

	
	Super::BeginPlay();
	//FVector a = FVector(250, 250, 250);
	//SetActorRelativeLocation(a);


	UDP_Init();
	
}
void AMyPen::UDP_Init() {

	bool success = true;
	StartUDPReceiver(RotationSocket, PenIP, RotaPort, success);
	StartUDPReceiver(LocationSocket, PenIP, LocaPort, success);


}

void AMyPen::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	Super::EndPlay(EndPlayReason);
	//~~~~~~~~~~~~~~~~


	//Clear all sockets!
	//      makes sure repeat plays in Editor dont hold on to old sockets!
	if (RotaSocket)
	{
		RotaSocket->Close();
		ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(RotaSocket);
	}
	if (LocaSocket)
	{
		LocaSocket->Close();
		ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->DestroySocket(LocaSocket);
	}
}
// Called every frame
void AMyPen::Tick(float DeltaTime)
{

	//UE_LOG(PenLog, Warning, TEXT("DeltaTime %f"),DeltaTime);
	Super::Tick(DeltaTime);
	
	DataRecvRota();
	DataRecvLoca();
	//UE_LOG(PenLog, Warning, TEXT("Pitch:%f,Yaw:%f,Roll:%f,"), Pitch, Yaw, Roll);
	FRotator rotator(Pitch,Yaw,Roll);
	SetActorRotation(rotator);
	FVector loca(X, Y, Z);
	SetActorLocation(loca);
	if (!CurrentVelocity.IsZero())
	{
		FVector NewLocation = GetActorLocation() + (CurrentVelocity * DeltaTime);
		SetActorLocation(NewLocation);
	}
}

// Called to bind functionality to input
void AMyPen::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
	InputComponent->BindAxis("MoveX", this, &AMyPen::Move_XAxis);
	InputComponent->BindAxis("MoveY", this, &AMyPen::Move_YAxis);
}


void AMyPen::StartUDPReceiver(const FString& YourChosenSocketName, const FString& TheIP, const int32 ThePort, bool& success) // 接收器初始化  接收信息前
{

	TSharedRef<FInternetAddr> targetAddr = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->CreateInternetAddr();
	FIPv4Address Addr;
	FIPv4Address::Parse(TheIP, Addr);

	//Create Socket
	FIPv4Endpoint Endpoint(FIPv4Address::Any, ThePort);
	ListenSocket = FUdpSocketBuilder(*YourChosenSocketName)
		.AsNonBlocking()
		.AsReusable()
		.BoundToEndpoint(Endpoint)
		.WithReceiveBufferSize(2 * 1024 * 1024)

		;
	//BUFFER SIZE
	int32 BufferSize = 2 * 1024 * 1024;
	ListenSocket->SetSendBufferSize(BufferSize, BufferSize);
	ListenSocket->SetReceiveBufferSize(BufferSize, BufferSize);
	if (YourChosenSocketName == "RotationSocket") {
		RotaSocket = ListenSocket;
	}
	if (YourChosenSocketName == "LocationSocket") {
		LocaSocket = ListenSocket;
	}

}

void AMyPen::DataRecvRota()              //接收消息处理
{
	//ScreenMsg("No sender socket");
	if (!RotaSocket)
	{
		ScreenMsg("No sender socket");
	}
	TSharedRef<FInternetAddr> targetAddr = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->CreateInternetAddr();
	TArray<uint8> ReceivedData;//定义一个接收器
	uint32 Size;
	if (RotaSocket->HasPendingData(Size))
	{
		
		FString str = "";
		uint8* Recv = new uint8[Size];
		int32 BytesRead = 0;
		ReceivedData.SetNumUninitialized(FMath::Min(Size, 65507u));
		RotaSocket->RecvFrom(ReceivedData.GetData(), ReceivedData.Num(), BytesRead, *targetAddr);//创建远程接收地址
		char ansiiData[1024];
		if (sizeof(ansiiData) < BytesRead) return;
		memcpy(ansiiData, ReceivedData.GetData(), BytesRead);//拷贝数据到接收器
		//ansiiData[BytesRead] = 0;                            //判断数据结束
		FString debugData = ANSI_TO_TCHAR(ansiiData);         //字符串转换
		str = debugData;
		memset(ansiiData,0,1024);//清空 
		//ScreenMsg(str);
		//UE_LOG(PenLog, Warning, TEXT("%s"), *str);
		TArray<FString> stringArray;
		str.ParseIntoArray(stringArray, TEXT("1073645562"), false);
		TArray<uint8> dataArray;
		std::vector<uint8> VecData;
		for (FString a : stringArray) {
			dataArray.Add(FCString::Atoi(*a));
			VecData.push_back(FCString::Atoi(*a));
		}
		LogUint8Array(dataArray);
		AnalyseUint8Array(VecData);
	}
	//return success;
}
void AMyPen::DataRecvLoca()              //接收消息处理
{
	//ScreenMsg("No sender socket");
	if (!LocaSocket)
	{
		ScreenMsg("No sender socket");
	}
	TSharedRef<FInternetAddr> targetAddr = ISocketSubsystem::Get(PLATFORM_SOCKETSUBSYSTEM)->CreateInternetAddr();
	TArray<uint8> ReceivedData;//定义一个接收器
	uint32 Size;
	if (LocaSocket->HasPendingData(Size))
	{
		FString str = "";
		uint8* Recv = new uint8[Size];
		int32 BytesRead = 0;
		ReceivedData.SetNumUninitialized(FMath::Min(Size, 65507u));
		LocaSocket->RecvFrom(ReceivedData.GetData(), ReceivedData.Num(), BytesRead, *targetAddr);//创建远程接收地址
		char ansiiData[1024];
		memcpy(ansiiData, ReceivedData.GetData(), BytesRead);//拷贝数据到接收器
		ansiiData[BytesRead] = 0;                            //判断数据结束
		FString debugData = ANSI_TO_TCHAR(ansiiData);         //字符串转换
		str = debugData;
		memset(ansiiData,0,1024);//清空 
		//ScreenMsg(str);
		UE_LOG(PenLog, Warning, TEXT("%s"), *str);
		TArray<FString> stringArray;
		str.ParseIntoArray(stringArray, TEXT("_"), false);
		TArray<double_t> dataArray;
		std::vector<double_t> VecData;
		for (FString a : stringArray) {
			dataArray.Add(FCString::Atof(*a));
			VecData.push_back(FCString::Atof(*a));
		}
		AnalyseXYZ(VecData);
	}
}

void AMyPen::LogUint8Array(TArray<uint8> dataArray) {
	FString data;
	for (auto i : dataArray) {
		char temp[1];
		itoa(i, temp, 16);
		data += temp;
		data += " ";
	}
	UE_LOG(PenLog, Warning, TEXT("redata %s"), *data);

}

void AMyPen::AnalyseXYZ(std::vector<double_t> dataArray) {
	X = dataArray[0];
	Y = dataArray[1];
	Z = dataArray[2];

}
void AMyPen::AnalyseUint8Array(std::vector<uint8> dataArray) {

	if (dataArray[23] != 0x53 && dataArray[22] != 0x55) return ;
	Roll = ((dataArray[25] << 8) | dataArray[24]) / 32768.0 * 180;
	Pitch = -((dataArray[27] << 8) | dataArray[26]) / 32768.0 * 180;
	Yaw =- ((dataArray[29] << 8) | dataArray[28]) / 32768.0 * 180;

	//UE_LOG(PenLog, Warning, TEXT("Pitch:%f,Yaw:%f,Roll:%f,"), Pitch, Yaw, Roll);
	Button0 = bool(dataArray[33]);
	Button1 = bool(dataArray[34]);
}
