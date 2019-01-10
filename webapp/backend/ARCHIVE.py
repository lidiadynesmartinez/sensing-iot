
avg_temp = [9, 8, 7, 7, 11, 7, 5, 8, 6, 2, 10, 8, 9, 11, 13, 14, 21, 12, 18, 20, 20, 23, 24, 23, 21, 24, 27, 28, 26, 26, 28, 29, 24, 22, 21, 23, 22, 21, 18, 18, 18, 19, 17, 12, 11, 14, 12, 7, 12, 11, 7, 10]
sunglasses = [21, 23, 21, 23, 26, 26, 30, 31, 30, 32, 35, 38, 40, 41, 43, 85, 61, 60, 89, 76, 80, 74, 71, 67, 62, 100, 94, 80, 73, 71, 59, 55, 40, 34, 30, 30, 24, 24, 24, 20, 19, 18, 20, 19, 16, 17, 21, 18, 16, 18, 17, 18]
gloves = [45, 53, 51, 45, 42, 52, 47, 46, 70, 46, 44, 45, 36, 34, 33, 31, 31, 31, 29, 29, 27, 28, 31, 30, 29, 28, 26, 28, 32, 28, 29, 30, 31, 32, 35, 36, 39, 41, 49, 48, 45, 49, 59, 82, 59, 58, 98, 93, 85, 100, 82, 51]
baked_beans = [93, 100, 100, 94, 86, 92, 86, 88, 85, 79, 85, 85, 75, 67, 85, 89, 95, 79, 71, 73, 77, 69, 81, 88, 76, 61, 67, 71, 77, 85, 79, 74, 75, 82, 80, 79, 80, 89, 83, 90, 87, 91, 84, 100, 89, 81, 72, 67, 66, 72, 59, 50]


# plt.figure(1, figsize=(20, 5))
# plt.plot(avg_temp)
# plt.plot(sunglasses)
# plt.ylabel('Raw Data')
# plt.show()


n_avg_temp = (avg_temp - np.mean(avg_temp))/np.std(avg_temp)
n_sunglasses = (sunglasses - np.mean(sunglasses))/np.std(sunglasses)
# plt.figure(2, figsize=(20, 5))
# plt.plot(n_avg_temp)
# plt.plot(n_sunglasses)
# plt.ylabel('Normalised Data')
# plt.show()


print(pearsonr(avg_temp, sunglasses))

variance_avg_temp = np.var(avg_temp)
variance_sunglasses = np.var(sunglasses)
print(variance_avg_temp, variance_sunglasses)

variance_n_avg_temp = np.var(n_avg_temp)
variance_n_sunglasses = np.var(n_sunglasses)
print(variance_n_avg_temp, variance_n_sunglasses)

print(np.corrcoef(avg_temp, sunglasses))
print(np.corrcoef(avg_temp, gloves))
print(np.corrcoef(avg_temp, baked_beans))

# plt.scatter(avg_temp, baked_beans)
# plt.show()
