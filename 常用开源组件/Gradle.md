##### 强制使用最新的版本，不使用缓存
```
configurations.all {
    resolutionStrategy.cacheDynamicVersionsFor(0, TimeUnit.SECONDS) // 动态版本 x.x.+
    resolutionStrategy.cacheChangingModulesFor(0, TimeUnit.SECONDS) //  变化版本 x.x.x
}
```

##### kotlin 1.2 升级 1.3报错

```
./gradlew dependencies --configuration kotlinCompilerClasspath
```

