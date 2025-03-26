"""
Author: WAADRI <https://github.com/WAADRI>
Date: 2025-03-26
"""

import math


class RSAUtils:
    def __init__(self):
        self.biRadixBase = 2
        self.biRadixBits = 16
        self.bitsPerDigit = self.biRadixBits
        self.biRadix = 1 << 16
        self.biHalfRadix = self.biRadix >> 1
        self.biRadixSquared = self.biRadix * self.biRadix
        self.maxDigitVal = self.biRadix - 1
        self.maxInteger = 9999999999999998
        self.maxDigits = self.ZERO_ARRAY = self.bigZero = self.bigOne = None
        self.setMaxDigits(20)
        self.dpl10 = 15
        self.lr10 = self.biFromNumber(1000000000000000)
        self.hexatrigesimalToChar = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]
        self.hexToChar = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
        self.highBitMasks = [
            0x0000,
            0x8000,
            0xC000,
            0xE000,
            0xF000,
            0xF800,
            0xFC00,
            0xFE00,
            0xFF00,
            0xFF80,
            0xFFC0,
            0xFFE0,
            0xFFF0,
            0xFFF8,
            0xFFFC,
            0xFFFE,
            0xFFFF,
        ]
        self.lowBitMasks = [
            0x0000,
            0x0001,
            0x0003,
            0x0007,
            0x000F,
            0x001F,
            0x003F,
            0x007F,
            0x00FF,
            0x01FF,
            0x03FF,
            0x07FF,
            0x0FFF,
            0x1FFF,
            0x3FFF,
            0x7FFF,
            0xFFFF,
        ]
        self.setMaxDigits(130)

    def BigInt(self, flag=None):
        result = {}
        if type(flag) is bool and flag is True:
            result["digits"] = None
        else:
            result["digits"] = self.ZERO_ARRAY.copy()
        result["isNeg"] = False
        return result

    def setMaxDigits(self, value):
        maxDigits = value
        self.ZERO_ARRAY = []
        for iza in range(maxDigits):
            self.ZERO_ARRAY.append(0)
        self.bigZero = {"digits": self.ZERO_ARRAY.copy(), "isNeg": False}
        self.bigOne = {"digits": self.ZERO_ARRAY.copy(), "isNeg": False}
        self.bigOne["digits"][0] = 1

    def biFromNumber(self, i):
        result = self.BigInt()
        result["isNeg"] = i < 0
        i = abs(i)
        j = 0
        while i > 0:
            result["digits"][j] = i & self.maxDigitVal
            j += 1
            i = math.floor(i / self.biRadix)
        return result

    def biFromDecimal(self, s):
        isNeg = s[0] == "-"
        i = 1 if isNeg else 0
        i += 1
        while i < len(s) and s[i] == "0":
            i += 1
        if i == len(s):
            result = self.BigInt()
        else:
            digitCount = len(s) - i
            fgl = digitCount % self.dpl10
            if fgl == 0:
                fgl = self.dpl10
            result = self.biFromNumber(float(s[i : i + fgl]))
            i += fgl
            while i < len(s):
                result = self.biAdd(
                    self.biMultiply(result, self.lr10), self.biFromNumber(float(s[i : i + self.dpl10]))
                )
                i += self.dpl10
            result.isNeg = isNeg
        return result

    def biCopy(self, bi):
        result = self.BigInt(True)
        bi["digits"] = bi["digits"].copy()
        result["digits"] = bi["digits"]
        result["isNeg"] = bi["isNeg"]
        return result

    def reverseStr(self, s):
        result = ""
        for i in range(len(s) - 1, -1, -1):
            result += s[i]
        return result

    def biToString(self, x, radix):
        b = self.BigInt()
        b["digits"][0] = radix
        qr = self.biDivideModulo(x, b)
        result = self.hexatrigesimalToChar[qr[1]["digits"][0]]
        while self.biCompare(qr[0], self.bigZero) == 1:
            qr = self.biDivideModulo(qr[0], b)
            result += self.hexatrigesimalToChar[qr[1]["digits"][0]]
        return ("-" if x["isNeg"] else "") + self.reverseStr(result)

    def biToDecimal(self, x):
        b = self.BigInt()
        b["digits"][0] = 10
        qr = self.biDivideModulo(x, b)
        result = str(qr[1]["digits"][0])
        while self.biCompare(qr[0], self.bigZero) == 1:
            qr = self.biDivideModulo(qr[0], b)
            result += str(qr[1]["digits"][0])
        return ("-" if x["isNeg"] else "") + self.reverseStr(result)

    def digitToHex(self, n):
        mask = 0xF
        result = ""
        for i in range(4):
            result += self.hexToChar[n & mask]
            n = (n & 0xFFFFFFFF) >> (4 & 0x1F)
        return self.reverseStr(result)

    def biToHex(self, x):
        result = ""
        for i in range(self.biHighIndex(x), -1, -1):
            result += self.digitToHex(x["digits"][i])
        return result

    def charToHex(self, c):
        ZERO = 48
        NINE = ZERO + 9
        littleA = 97
        littleZ = littleA + 25
        bigA = 65
        bigZ = 65 + 25
        if NINE >= c >= ZERO:
            result = c - ZERO
        elif bigZ >= c >= bigA:
            result = 10 + c - bigA
        elif littleZ >= c >= littleA:
            result = 10 + c - littleA
        else:
            result = 0
        return result

    def hexToDigit(self, s):
        result = 0
        sl = min(len(s), 4)
        for i in range(0, sl):
            result <<= 4
            result |= self.charToHex(ord(s[i]))
        return result

    def biFromHex(self, s):
        result = self.BigInt()
        sl = len(s)
        i = sl
        j = 0
        while i > 0:
            result["digits"][j] = self.hexToDigit(s[max(i - 4, 0) : max(i - 4, 0) + min(i, 4)])
            i -= 4
            j += 1
        return result

    def biFromString(self, s, radix):
        isNeg = s[0] == "-"
        istop = 1 if isNeg else 0
        result = self.BigInt()
        place = self.BigInt()
        place["digits"][0] = 1
        for i in range(len(s) - 1, istop - 1, -1):
            c = ord(s[i])
            digit = self.charToHex(c)
            biDigit = self.biMultiplyDigit(place, digit)
            result = self.biAdd(result, biDigit)
            place = self.biMultiplyDigit(place, radix)
        result["isNeg"] = isNeg
        return result

    def biDump(self, b):
        return ("-" if b["isNeg"] else "") + " ".join(b["digits"])

    def biAdd(self, x, y):
        if x["isNeg"] != y["isNeg"]:
            y["isNeg"] = not y["isNeg"]
            result = self.biSubtract(x, y)
            y["isNeg"] = not y["isNeg"]
        else:
            result = self.BigInt()
            c = 0
            for i in range(1, len(x["digits"])):
                n = x["digits"][i] + y["digits"][i] + c
                result["digits"][i] = n % self.biRadix
                c = float(n >= self.biRadix)
            result["isNeg"] = x["isNeg"]
        return result

    def biSubtract(self, x, y):
        if x["isNeg"] != y["isNeg"]:
            y["isNeg"] = not y["isNeg"]
            result = self.biAdd(x, y)
            y["isNeg"] = not y["isNeg"]
        else:
            result = self.BigInt()
            c = 0
            for i in range(0, len(x["digits"])):
                n = x["digits"][i] - y["digits"][i] + c
                result["digits"][i] = n % self.biRadix
                if result["digits"][i] < 0:
                    result["digits"][i] += self.biRadix
                c = int(0 - float(n < 0))
            if c == -1:
                c = 0
                for i in range(1, len(x["digits"])):
                    n = 0 - result["digits"][i] + c
                    result["digits"][i] = n % self.biRadix
                    if result["digits"][i] < 0:
                        result["digits"][i] += self.biRadix
                    c = int(0 - float(n < 0))
                result["isNeg"] = not x["isNeg"]
            else:
                result["isNeg"] = x["isNeg"]
        return result

    def biHighIndex(self, x):
        result = len(x["digits"]) - 1
        while result > 0 and x["digits"][result] == 0:
            result -= 1
        return result

    def biNumBits(self, x):
        n = self.biHighIndex(x)
        d = x["digits"][n]
        m = (n + 1) * self.bitsPerDigit
        result = None
        for result in range(m, m - self.bitsPerDigit - 1, -1):
            if d & 0x8000 != 0:
                break
            d <<= 1
        return result

    def biMultiply(self, x, y):
        result = self.BigInt()
        n = self.biHighIndex(x)
        t = self.biHighIndex(y)
        for i in range(t + 1):
            c = 0
            k = i
            for j in range(n + 1):
                uv = result["digits"][k] + x["digits"][j] * y["digits"][i] + c
                result["digits"][k] = uv & self.maxDigitVal
                c = (uv & 0xFFFFFFFF) >> (self.biRadixBits & 0x1F)
                k += 1
            result["digits"][i + n + 1] = c
        result["isNeg"] = x["isNeg"] != y["isNeg"]
        return result

    def biMultiplyDigit(self, x, y):
        result = self.BigInt()
        n = self.biHighIndex(x)
        c = 0
        for j in range(n + 1):
            uv = result["digits"][j] + x["digits"][j] * y + c
            result["digits"][j] = uv & self.maxDigitVal
            c = (uv & 0xFFFFFFFF) >> (self.biRadixBits & 0x1F)
        result["digits"][1 + n] = c
        return result

    def arrayCopy(self, src, srcStart, dest, destStart, n):
        m = min(srcStart + n, len(src))
        j = destStart
        for i in range(srcStart, m):
            dest[j] = src[i]
            j += 1

    def biShiftLeft(self, x, n):
        digitCount = math.floor(n / self.bitsPerDigit)
        result = self.BigInt()
        self.arrayCopy(x["digits"], 0, result["digits"], digitCount, len(result["digits"]) - digitCount)
        bits = n % self.bitsPerDigit
        rightBits = self.bitsPerDigit - bits
        i = len(result["digits"]) - 1
        i1 = i - 1
        for i in range(len(result["digits"]) - 1, 0, -1):
            result["digits"][i] = ((result["digits"][i] << bits) & self.maxDigitVal) | (
                ((result["digits"][i1] & self.highBitMasks[bits]) & 0xFFFFFFFF) >> (rightBits & 0x1F)
            )
            i1 -= 1
        result["digits"][0] = (result["digits"][i] << bits) & self.maxDigitVal
        result["isNeg"] = x["isNeg"]
        return result

    def biShiftRight(self, x, n):
        digitCount = math.floor(n / self.bitsPerDigit)
        result = self.BigInt()
        self.arrayCopy(x["digits"], digitCount, result["digits"], 0, len(x["digits"]) - digitCount)
        bits = n % self.bitsPerDigit
        leftBits = self.bitsPerDigit - bits
        i = 0
        i1 = i + 1
        for i in range(len(result["digits"]) - 1):
            result["digits"][i] = (result["digits"][i] >> bits) | (
                (result["digits"][i1] & self.lowBitMasks[bits]) << leftBits
            )
            i1 += 1
        result["digits"][len(result["digits"]) - 1] >>= bits
        result["isNeg"] = x["isNeg"]
        return result

    def biMultiplyByRadixPower(self, x, n):
        result = self.BigInt()
        self.arrayCopy(x["digits"], 0, result["digits"], n, len(result["digits"]) - n)
        return result

    def biDivideByRadixPower(self, x, n):
        result = self.BigInt()
        self.arrayCopy(x["digits"], n, result["digits"], 0, len(result["digits"]) - n)
        return result

    def biModuloByRadixPower(self, x, n):
        result = self.BigInt()
        self.arrayCopy(x["digits"], 0, result["digits"], 0, n)
        return result

    def biCompare(self, x, y):
        if x["isNeg"] != y["isNeg"]:
            return 1 - 2 * float(x["isNeg"])
        for i in range(len(x["digits"]) - 1, -1, -1):
            if x["digits"][i] != y["digits"][i]:
                if x["isNeg"]:
                    return 1 - 2 * float(x["digits"][i] > y["digits"][i])
                else:
                    return 1 - 2 * float(x["digits"][i] < y["digits"][i])
        return 0

    def biDivideModulo(self, x, y):
        nb = self.biNumBits(x)
        tb = self.biNumBits(y)
        origYIsNeg = y["isNeg"]
        if nb < tb:
            if x["isNeg"]:
                q = self.biCopy(self.bigOne)
                q["isNeg"] = not y["isNeg"]
                x["isNeg"] = False
                y["isNeg"] = False
                r = self.biSubtract(y, x)
                x["isNeg"] = True
                y["isNeg"] = origYIsNeg
            else:
                q = self.BigInt()
                r = self.biCopy(x)
            return [q, r]
        q = self.BigInt()
        r = x
        t = math.ceil(tb / self.bitsPerDigit) - 1
        _lambda = 0
        while y["digits"][t] < self.biHalfRadix:
            y = self.biShiftLeft(y, 1)
            _lambda += 1
            tb += 1
            t = math.ceil(tb / self.bitsPerDigit) - 1
        r = self.biShiftLeft(r, _lambda)
        nb += _lambda
        n = math.ceil(nb / self.bitsPerDigit) - 1
        b = self.biMultiplyByRadixPower(y, n - t)
        while self.biCompare(r, b) != -1:
            q["digits"][n - t] += 1
            r = self.biSubtract(r, b)
        for i in range(n, t, -1):
            ri = 0 if i >= len(r["digits"]) else r["digits"][i]
            ri1 = 0 if i - 1 >= len(r["digits"]) else r["digits"][i - 1]
            ri2 = 0 if i - 2 >= len(r["digits"]) else r["digits"][i - 2]
            yt = 0 if t >= len(y["digits"]) else y["digits"][t]
            yt1 = 0 if t - 1 >= len(y["digits"]) else y["digits"][t - 1]
            if ri == yt:
                q["digits"][i - t - 1] = self.maxDigitVal
            else:
                q["digits"][i - t - 1] = math.floor((ri * self.biRadix + ri1) / yt)
            c1 = q["digits"][i - t - 1] * ((yt * self.biRadix) + yt1)
            c2 = (ri * self.biRadixSquared) + ((ri1 * self.biRadix) + ri2)
            while c1 > c2:
                q["digits"][i - t - 1] -= 1
                c1 = q["digits"][i - t - 1] * ((yt * self.biRadix) | yt1)
                c2 = (ri * self.biRadix * self.biRadix) + ((ri1 * self.biRadix) + ri2)
            b = self.biMultiplyByRadixPower(y, i - t - 1)
            r = self.biSubtract(r, self.biMultiplyDigit(b, q["digits"][i - t - 1]))
            if r["isNeg"]:
                r = self.biAdd(r, b)
                q["digits"][i - t - 1] -= 1
        r = self.biShiftRight(r, _lambda)
        q["isNeg"] = x["isNeg"] != origYIsNeg
        if x["isNeg"]:
            if origYIsNeg:
                q = self.biAdd(q, self.bigOne)
            else:
                q = self.biSubtract(q, self.bigOne)
            y = self.biShiftRight(y, _lambda)
            r = self.biSubtract(y, r)
        if r["digits"][0] == 0 and self.biHighIndex(r) == 0:
            r["isNeg"] = False
        return [q, r]

    def biDivide(self, x, y):
        return self.biDivideModulo(x, y)[0]

    def biModulo(self, x, y):
        return self.biDivideModulo(x, y)[1]

    def biMultiplyMod(self, x, y, m):
        return self.biModulo(self.biMultiply(x, y), m)

    def biPow(self, x, y):
        result = self.bigOne
        a = x
        while True:
            if (y & 1) != 0:
                result = self.biMultiply(result, a)
            y >>= 1
            if y == 0:
                break
            a = self.biMultiply(a, a)
        return result

    def biPowMod(self, x, y, m):
        result = self.bigOne
        a = x
        k = y
        while True:
            if (k["digits"][0] & 1) != 0:
                result = self.biMultiplyMod(result, a, m)
            k = self.biShiftRight(k, 1)
            if k["digits"][0] == 0 and self.biHighIndex(k) == 0:
                break
            a = self.biMultiplyMod(a, a, m)
        return result

    def BarrettMu(self, m):
        self.modulus = self.biCopy(m)
        self.k = self.biHighIndex(self.modulus) + 1
        b2k = self.BigInt()
        b2k["digits"][2 * self.k] = 1
        self.mu = self.biDivide(b2k, self.modulus)
        self.bkplus1 = self.BigInt()
        self.bkplus1["digits"][self.k + 1] = 1
        self.modulo = self.BarrettMu_modulo
        self.multiplyMod = self.BarrettMu_multiplyMod
        self.powMod = self.BarrettMu_powMod
        return self

    def BarrettMu_modulo(self, x):
        q1 = self.biDivideByRadixPower(x, self.k - 1)
        q2 = self.biMultiply(q1, self.mu)
        q3 = self.biDivideByRadixPower(q2, self.k + 1)
        r1 = self.biModuloByRadixPower(x, self.k + 1)
        r2term = self.biMultiply(q3, self.modulus)
        r2 = self.biModuloByRadixPower(r2term, self.k + 1)
        r = self.biSubtract(r1, r2)
        if r["isNeg"]:
            r = self.biAdd(r, self.bkplus1)
        rgtem = self.biCompare(r, self.modulus) >= 0
        while rgtem:
            r = self.biSubtract(r, self.modulus)
            rgtem = self.biCompare(r, self.modulus) >= 0
        return r

    def BarrettMu_multiplyMod(self, x, y):
        xy = self.biMultiply(x, y)
        return self.modulo(xy)

    def BarrettMu_powMod(self, x, y):
        result = self.BigInt()
        result["digits"][0] = 1
        a = x
        k = y
        while True:
            if (k["digits"][0] & 1) != 0:
                result = self.multiplyMod(result, a)
            k = self.biShiftRight(k, 1)
            if k["digits"][0] == 0 and self.biHighIndex(k) == 0:
                break
            a = self.multiplyMod(a, a)
        return result

    def RSAKeyPair(self, encryptionExponent, decryptionExponent, modulus):
        self.e = self.biFromHex(encryptionExponent)
        self.d = self.biFromHex(decryptionExponent)
        self.m = self.biFromHex(modulus)
        self.chunkSize = 2 * self.biHighIndex(self.m)
        self.radix = 16
        self.barrett = self.BarrettMu(self.m)

    def getKeyPair(self, encryptionExponent, decryptionExponent, modulus):
        this = RSAUtils()
        this.setMaxDigits(400)
        this.RSAKeyPair(encryptionExponent, decryptionExponent, modulus)
        return this

    def twoDigit(self, n):
        return ("0" if n < 10 else "") + str(n)

    def encryptedString(self, key, s):
        a = []
        sl = len(s)
        for st in range(sl):
            a.append(None)
        i = 0
        while i < sl:
            a[i] = ord(s[i])
            i += 1
        while len(a) % key.chunkSize != 0:
            a.append(0)
            i += 1
        al = len(a)
        result = ""
        for i in range(0, al, key.chunkSize):
            block = self.BigInt()
            k = i
            j = 0
            while k < i + key.chunkSize:
                block["digits"][j] = a[k]
                k += 1
                while len(a) < k + 1:
                    a.append(0)
                block["digits"][j] += a[k] << 8
                k += 1
                j += 1
            crypt = key.barrett.powMod(block, key.e)
            text = self.biToHex(crypt) if key.radix == 16 else self.biToString(crypt, key.radix)
            result += text + " "
        return result[0 : len(result) - 1]

    def decryptedString(self, key, s):
        blocks = s.split(" ")
        result = ""
        for i in range(len(blocks)):
            if key.radix == 16:
                bi = self.biFromHex(blocks[i])
            else:
                bi = self.biFromString(blocks[i], key.radix)
            block = key.barrett.powMod(bi, key.d)
            for j in range(self.biHighIndex(block)):
                result += "".join(chr(code) for code in [block["digits"][j] & 255, block["digits"][j] >> 8])
        if ord(result[len(result) - 1]) == 0:
            result = result[0 : len(result) - 1]
        return result


def encryptedPassword(password):
    password_reverse_list = []
    for p in password:
        password_reverse_list.insert(0, p)
    passwordEncode = "".join(password_reverse_list)
    publicKeyExponent = "10001"
    publicKeyModulus = "94dd2a8675fb779e6b9f7103698634cd400f27a154afa67af6166a43fc26417222a79506d34cacc7641946abda1785b7acf9910ad6a0978c91ec84d40b71d2891379af19ffb333e7517e390bd26ac312fe940c340466b4a5d4af1d65c3b5944078f96a1a51a5a53e4bc302818b7c9f63c4a1b07bd7d874cef1c3d4b2f5eb7871"
    this = RSAUtils()
    this.setMaxDigits(400)
    key = this.getKeyPair(publicKeyExponent, "", publicKeyModulus)
    passwordEncry = this.encryptedString(key, passwordEncode)
    return passwordEncry
