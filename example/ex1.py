help()

bctype(2)

setLoading('triangle')
setLoadingParameterValues([10,0.005])

setConstitutive('maxwell')
setConstitutiveParameterValues([200,3000])

solve()
plot()
