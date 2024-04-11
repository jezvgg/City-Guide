FROM mcr.microsoft.com/dotnet/aspnet:9.0-preview AS base
USER app
WORKDIR /app
EXPOSE 8080

FROM mcr.microsoft.com/dotnet/sdk:9.0-preview AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["./uTraverse.AiAPI.csproj", "uTraverse.AiAPI/"]
RUN dotnet restore "./uTraverse.AiAPI.csproj"
COPY . .
WORKDIR "/src/uTraverse.AiAPI"
RUN dotnet build "./uTraverse.AiAPI.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./uTraverse.AiAPI.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "uTraverse.AiAPI.dll"]