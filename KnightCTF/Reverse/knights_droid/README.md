# Knight's Droid

Description:

> For ages, a cryptic mechanical guardian has slumbered beneath the Knight’s Citadel. Some say it holds powerful secrets once wielded by ancient code-wielding Knights. Many have tried to reactivate the droid and claim its hidden knowledge—yet none have returned victorious. Will you be the one to solve its riddles and awaken this legendary machine?

Here, we have a some APK file. Let's open it with `Android Studio` (you can use other tools for .apk files):

![alt text](image.png)

Let's take a look at `com.knightctf` folder:

![alt text](image-1.png)

`SecretKeyVerifier` looks very strange and maybe it contains a logic to get the flag:

![alt text](image-2.png)

So, it has several important strings. They can be parts of the flag:

![alt text](image-3.png)

Now, we can try to make a whole string or deepen into the logic and look what is going on down there:

![alt text](image-4.png)

We have a whole string. Let's try to determine what kind of encryption it is using awesome website [dcode.fr](https://www.dcode.fr/cipher-identifier):

![alt text](image-5.png)

Let's try `ROT Cipher` decrypting:

![alt text](image-6.png)

Oh, we got it: `KCTF{_congrat5_KNIGHT_y0u_g0t_yOuR_Kn1gh7_dR01d_}`
