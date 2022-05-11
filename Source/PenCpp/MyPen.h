// Fill out your copyright notice in the Description page of Project Settings.

#pragma once
#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include <vector>
#include "MyPen.generated.h"

UCLASS()
class PENCPP_API AMyPen : public APawn
{
	GENERATED_BODY()
public:
	// Sets default values for this pawn's properties
	AMyPen();



	FORCEINLINE void ScreenMsg(const FString& Msg)
	{
		GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Red, *Msg);
	}
	FORCEINLINE void ScreenMsg(const FString& Msg, const float Value)
	{
		GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Red, FString::Printf(TEXT("%s %f"), *Msg, Value));
	}
	FORCEINLINE void ScreenMsg(const FString& Msg, const FString& Msg2)
	{
		GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Red, FString::Printf(TEXT("%s %s"), *Msg, *Msg2));
	}
protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:
	// Called every frame
	virtual void Tick(float DeltaTime) override;
	void LogUint8Array(TArray<uint8> dataArray);
	void AnalyseUint8Array(std::vector<uint8> dataArray);
	void AnalyseXYZ(std::vector<double_t> dataArray);
	void UDP_Init();

	// Called to bind functionality to input
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;
	UPROPERTY(EditAnywhere)
		USceneComponent* OurVisibleComponent;
	UPROPERTY(EditAnywhere)
		bool Button0=0;
	UPROPERTY(EditAnywhere)
		bool Button1=0;

	UFUNCTION(BlueprintCallable, Category = "MyFunc")
	bool GetButtonValue(bool but);
	//输入函数
	void Move_XAxis(float AxisValue);
	void Move_YAxis(float AxisValue);


	//UDP使用的参数
public:
	void StartUDPReceiver(const FString& YourChosenSocketName, const FString& TheIP, const int32 ThePort, bool& success);
	void DataRecvRota();
	void DataRecvLoca();
	//输入变量
	FSocket* ListenSocket;

	FSocket* RotaSocket;
	FSocket* LocaSocket;

	FString RotationSocket = "RotationSocket";
	FString LocationSocket = "LocationSocket";

	int32 RotaPort = 8888;
	int32 LocaPort = 9999;

	FString PenIP = "0.0.0.0";


	FVector CurrentVelocity;
	FSocket* UdpSocket;
	double Roll = 0;
	double Pitch = 0;
	double Yaw = 0;
	double X = 0;
	double Y = 0;
	double Z = 0;

	virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

};
