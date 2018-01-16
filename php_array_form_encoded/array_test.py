import requests, urllib.parse, urllib, sys
from to_php_post_arr.convert import recursive_urlencode
from urlencoder import urlencode

def recursive_urlencode(data):
    def r_urlencode(data, parent=None, pairs=None):
        if pairs is None:
            pairs = {}
        if parent is None:
            parents = []
        else:
            parents = parent

        for key, value in data.items():
            if hasattr(value, 'values'):
                parents.append(key)
                r_urlencode(value, parents, pairs)
                parents.pop()
            else:
                pairs[renderKey(parents + [key])] = renderVal(value)

        return pairs
    return urllib.parse.urlencode(r_urlencode(data))


def renderKey(parents):
    depth, outStr = 0, ''
    for x in parents:
        str = "[%s]" if depth > 0 else "%s"
        outStr += str % renderVal(x)
        depth += 1
    return outStr


def renderVal(val):
    return urllib.parse.quote(str(val))


def http_build_query(data):
    parents = list()
    pairs = dict()

    def renderKey(parents):
        depth, outStr = 0, ''
        for x in parents:
            s = "[%s]" if depth > 0 or isinstance(x, int) else "%s"
            outStr += s % str(x)
            depth += 1
        return outStr

    def r_urlencode(data):
        if isinstance(data, list) or isinstance(data, tuple):
            for i in range(len(data)):
                parents.append(i)
                r_urlencode(data[i])
                parents.pop()
        elif isinstance(data, dict):
            for key, value in data.items():
                parents.append(key)
                r_urlencode(value)
                parents.pop()
        else:
            pairs[renderKey(parents)] = str(data)

        return pairs
    return urllib.parse.urlencode(r_urlencode(data))

auth_token = 'bearer 1LzHxK8H08Iej-D2NTa_jF4pYHIpVvKazlJRXrlh0DxyiDyCCs1EH2ap9taOQfQ7mQUjAgghzV_v0_5dbqFh3NxjFan6kHS8_IND2v6xgq7jVxlhzj-__7gLtUc7rtLNgff5FZRkrp3TumvHkMQpoK5T-MJHnuYl-i6r5Mvm6uQvNcn3ZQpWwSapK4umWGXX5HQJeVu_krq__QVzcf_ZaF6i5yqlBcEoaaHtT2G2KsXBGQ9FGICitbEoULN7A0PF8uPtn7emH-MMkNuocKXcUTAghlcrDtutmILPQPq-EIdolCkIU7BFpxDDci_tWSfOfdL6nefECtdyg3QZ1JNQsaSmD1sRf1WKpH0dzhL-SnwOKAyXecPgtI82_4Iuau9XgL8d-6bkuPA6-jSANXuj2jwdchWiQYJMj1pPeTqK9Mk5bkOKWV_lPQTOc2KzbiUq2GPqJDo0mAvQpBLE3rrigWPEcAApV2m8C3hNer0UVMwgzZAGepiP9uK9vTvTm1w93sAX1eu7PoUjAse-t_CWy1Ncq4Jbyi8naq0BQ37CHLPMVHzn5wKzejh17N6SVxL_0RYoZIyMB5Lkz_zal8YQmfRI7s8FZdX_CQbzyfnz-oYAiHHSMNSO0KZxvrZ8qhcA3_IXOvg48Cbqe7fFvpXTv4iUZYLblJPvc_itnOLHQ-RST9Dcw0FpvYg8GcKco6O2bZd2QhcZELVwrNZlowiK7iLIVJWwQDvgJ7SGPwciGbhnXLOBwWeDLEMFGiQ8IQTIx3Qkc4fo7dzG9613t-tu-vciRchTEpWccj3tihJvvq9B4-MTIFLdfcCsL-jD9ypV3AdHebzgLDt4_jTtfk4TjYvB9Q_caepuhZsbi1d4l7IoamGAUnbPnZWZypicJjWQOSnySuZS1pnuoUUd8mqlMz62w4WNXZwCK1b-GXMAt0I5RNhS5clFFQWz1JIwPmxoLav7Gr8QJDnknFMqwDp51SJH3TRk7L5f-aPDUEtpSSgVoBvAkiFy4tpDJdF_WtcTb3JNCeQnqaokeD2SGIdcFYK45c1Nrv9yVGLAhnjKKqCLn2tbzPhYmTL6tWhu3DLgtN0ExIlwmux6awtMMvolPULk7FE7W9wBzy8rRjagDfrA-pEL6Tuqdh9ffWKVQB4D0Zui3K7L2ZD73i4C3rZB40krcInHDyQXDgH0e7QxHFy0NwyzPAv5U8QRXrawj_rWnNwdLWaKnnpXPIIb0urYAF6U85phLFfN2r7ucuktIq71PpquyjjikA1mhvH8IhaGc2F3_1IswCy5e05nNQz1WXZX1gSmvJi1XzCxw5aHd8U9QF91s2dAYpuXwK5uidaqW1WGUKVdcOWrAUcCea8Y29Nr3k7uvWC7C_nfwQj-MGWUa8ivj805tB77ELBaws_7ulz4uJnmQWoHfeEVDVp-50fDy-rgoy0HZ3-osFMl9mZWHn_C62hA6NXCEvUxuI4sn_Tex49_q4WnIhhPSyvadKc-ShKw1kRF5cTD5vt_EC6N97-mCKfkgGXLEGRvY5BD3e4XPNuhxLzeBUxfC0XWVpqQlpkSZOHSJeTGnJ_Jy7peKNEY1Ut9EXiO3AbgJdKlpmJj-vAlfnLSAmLztrPRs0rjnTA_6q62y_iroV64u99ulx_jaarbTX0fbaG-e5mwc8tWzgqRmgHZofVonw4LeUVEnMqmH9Nvxoy3rsAC21QVkyl4aY6v28sy93lLg7qPyYDdiKlHqp-nzY6-8uv-lXR59HoGtrGeYoIrqzeXc5dCC0pJFBS1jJZArcU3E81BgnGhObacs5SQ3HvGyE4IxC278KIhClx21vURP2kEqydl9kGdAVUTsHdMXmw1bPG1h-XSZGzeeEcA00kGFxDOIaLuVSZHiQ54Et20dfOoJFvTP8t35VKQf-nMBWslp7Vzkv3hQMm5mayqJwxAEyc2uY_wNuTUpqfWqzZT4dREMY6ovio2MPFFj-YnZEZuCjYzHdkswjW1_yVznutBeyC2ryqCm5XXSM3EFxyeTOA7Efjtb3O4JP59ixhY8bx_iB93K1wXTtVv3O_b6Zp6mynseePUZU_JyA3r5SXofTm2GhoyIDgezdPyeK44xvxOVYm_7USYC0Q0HqJI1UMTpfxTCnaxoIJzS0T7sKHBA4ylTzhI9yhIltRlxy3S-Z2bsYChXtEVbSb5R2PXAoM2rNYUXR2hIsqxF-BkW-ozRozgIuPcJOeP_PX3J4O3bTsGDj4otrLIJViQLPYW-yK5iKGoWZeML6O72AOkwXJfqQ709yyGHcNPTtgIWmNxYTvxz8fEozr-jWlxlgxTtI82An6wctDYCajh3RuYMA5yA-iYsOMF0rFyt7Yilj2xWeV5ag3j2DO7XwbrltiB3G9FbnFbPcwakik6VEFfb3KC0T4cHy7Xh2238ipOTaDnY_6BxmSY4-3810XdW9IAodxmLcWzgKxac-hYJstAPF3h5CGjZ7gZv8FvyRILHryvnuyznPFgJaPziI_F3C2aFbdAkA8VI_2yfg7A0UlLFOA9UMOn30au_qhybWguiPjLPlsggARsObKX2fM-pQHeRohwKSDOl_NPxIiH_3Rf5Ahe-P06dmoOzZcGU_9lBFirU5vzoxIi9No5LP7vKLE7cTq2lgfw4bGfbSakFDG47T3s-1MsgbIKMFWaWipOJr7sgMzEsb5em1Bim8CVNIm1O3bF8qbYj7aFvMXvvdtu_XYZzsS3rQ8bnycgf1lA_XyUf6ON6LAufG9VoWkf4dSk4tPWjiADjqeKegq3RmBF7VXEOtecjkBZM9BxL8n-YZKljL8XSp4xmNmuO9qAYTtCtv88ZQ3V92Gv6vFFEzY1nSSO8iyAaBGnfh38SyKCnGxU9-jnkKPzcnStz1Qjdn-YMYEr3k_u63Z17IMIw41GCl_44VLuJBmIEjhZ7z_4XltoO624COE6u5yJRlLNKfYKgzuPwm1SbUDRgYz1ZoY0RhMBtQL5-gyQDJPmItLSQU7Md-trgg4f3DInJVPiu3wOBxBMo8ThYKEzdczmWaDzcRP4o3psEBd_l9rlYIX94kJU12DhIruc9_EN72JmF1gdhH6NrCIr5_9skBtLoz1Au-0YO4fPHhAMy5rG7T6-FjYjhWDEq_tMFEp9hcsWDNepETicVR3kJF4ckxDvegWlkgnxpyA1VmPLn4sNNGatN2GHxusenQlvEbg9uIOeIFIRmNDQ5l2GwDsAw5vtdlul1JPnqQ8zIQqT06g9LozJaPQn12WZxDVq0PyxJJ2yYkDMK6AcHXeavF9LXY2ntTVewtaJ4SSf4UyU-RbGssmzAGk2B3inyT3o0bA6biBoZjGzSLduhGmfzR2GBsSfud0n4xrE6R_ev5Mfa_3GaU-vDF0PRYqJxitYAkSIfqe5mIC9PNjZVXZPkQLLV37yPO-mZX9c9MH8oyaqvdmkzUiGTAt599OsdglTj_lnPYHJnL9GxTVzF-NjcRrTxbcgUe_-44hG5VsNcg2bWFbjAsJmixg7aVxTolEge8Ej0warFsRoKgDVwfwFVrBK0xHk7jQ7SZSniy_ABwjgvg0TF8s2JfAzuMX3YaiGtHO_-lC12Mw3WTn-3DXS67gIrCwcMpYMAoCW4TsRnI0e5KWM3XfrgpqQcaGffQadbk7d0Lq2QKShKjwK-OY3izV8JXh9nfp5Hp8XvITHH9iF7E23ht5NwyYJueuzwF3KtgRR5VYUe5CNpGSgS0-_T1RTMIm8SLS_8KPfk_D-XpDvIHc_wIMZ8HqlHWjHaU69LAEZlkE5XFfEHiaqE6f9DtDxXe5j_-wxLEl_gTldusGjN2Tz7hvldvL05jngooM2MhPLt2Lxathxn6x0RrYQQmFwnVeDUD9zCXrrZ7fZ__7ewItXr4m6UTTLtaDhpIXPEKrNHKddbNbIQyMCCTwO4_MESQqZff1Pg-zoUWT_i0LK_s8uoPVrsw6cAtks6vVmTdH_e7IOQGl21jotbY0KCJV0lKUNAnbxOz-oJX3leDfPe_rW-THnrruDQM6ZAXbCOG2TMR73wpWy21wOvNp9CP_AHD3SIPzgMocrpA90XADdFQOJcUFQ8ccMVNNDZNf6coXOHNDz5MbT93Bi2Fkz58U-G9wO12kX6NXoC07pnzY7xFpGD60KtN95BOhQ33s5cY3lmmuDKGM9YW42UYeCPqSLVX-e5jziXhANZkWjJFKt3gwaOI_tCgyvWJggaehym3QxG31_uNlpcJCzXbUMOMk1paUU68VC3eOsyJBsl6VYorle77uDSd_aQbWUr3-Q4u_Di1henCslw42odpLJ3OW9OYwZ6ojFZ8bCrOGFU13j63IiVUhd8G1fQdhnhO8dIkxkqhNpH7rZgXGa2XEC1XQQFLsNs7opzYjBPoHR22976oHSVru5d4FnpCuqwp46A8SAw9tHWG9QZzHDsc9w6_Qzie2qOrUFdQSe42EC5AomQBI0aH7-q8tUVnDlsQzIo5ENfq-MdA5GXWXETiBs8_76uOxpyJ0orJoTr8zjkSOe0NgxswY_t5CEBZWt3MrPffUMPHvgUHwPzqax9LreA0HUki7CZcxYkxt7vV9dmYQyva05hr-X_9JD-nd1qCGIfnloIwSRpgFxPYcduDnCAlW8IpJAfkw2sjrmy4Qr0SNBMek74lj8bnpgKW3Dq0kPwp8nrbDnG1xRBReym-k8MSlk3QpaZC3eRyabkQziHeoacun7Yw4OlDk3zPF8GR2R4U9hB8QujfIxV92YnKwPG4GQFmMFhh6VvVvWmNLOM1f5fVw0ul1a4Ga_QlljJ9229aGq_CGtk4Koi1QiJ6xLTA45Kx9Tle7KqpihyyyKTiBWNxtwetZtVa5aU2ofoaBlQtq89k-Y9jaG7j01TvX07YGRT7DxNik6nOx8KNkJtXKgbIo-TdaDeysPNgH1nwLVEy8A4iKFWK2bwjDDhXVvrHk5RpF0X3A1DPpHsMOOb5YauQZkyty1Kslm-HuYpWlHbW5ULxnam80dhV1blgjgckz6cg-GsT_eQhbEe9_c-Wy1xX9nNdeJuUtYRHrsEMtHGvvzNbWxmJP4YhPwSBM5-57uPmClIa7fyiCSahkRnGbBsB-oXiRiJw5DDKyFkU8o2gPsosK9FMpJB50vw3pDTCIw95HUXc4pv8TCKAm_HyAvqoDSQSf2hIkcXrlzoSYVA8c7JrxFWm0w8l9iXJlS8zrWE51NooDOc8UIXEGs2H0S9BJd-oZlZlDquVhhhwGAr-synpqew6K4UxSrT-rveID1gqzF5akquvRw5tDcOd3Oyg8uMdxA9hyuW23pkxPskUpnm2378t16yu9Y5qhyiXb9k1Ai_kOKCOA6pKsdQmnXyp81C09rJXf0aITBqUsScdFtV7j9hKKpUaELJBQIzm7mDOYpw6QSWz6Cq7azTE7AxYMCvpQbJIXz1-VfQz5BKNI8jQGtU4gB3aBsBwxGhVnjMjA5xKAk3E9Z85ctbbdJ98GrUqwjUtKP7sQZlTwbP3meGalVYUS6N46PT_6yDHt5ASXaUjK6k0B0A0nc2cp12khKvEgH3VGBN78UrAZs-iIzTAZbNS_qy0SkgS50qBRrZ1x1UsZXkUrwqmd81W7Ulor0UYc0fdZG-88l2wsTQ4PiDJdOM2l5O-aSVozM-6zX6KvYjg-QfqoFLshQWoCIK3vx2MV40Su887snOyYR7XKBtwOyKKm7ddOCjg0Ti2i1GmtrZYQtJYfnbqN6vys4otE6TBaFApcmyUo8VZ-XYOX84rHoFre-gOR2IIEpFUUu8c5b2B6jwrMkvNFkhmnj3Knh3qPkKFoItqxHzBNIXqpgM_ZUopuqTUArlhUml2cQkRs_Q6BX4jZBBPmhEvker0Vnuc4NkWfwKWCmXZlh6rseTwzN6CbgwGg5-2213KUpKf0rjO2FqctRscm2oWTwfD_bsxlZGOLgbEyqd2jTC_sFIjx30FTUWRWMHcwNx6PtpzZg7NTuCnugTsamtOs'

headers = {'Authorization': auth_token, 'app_key': 'BBD14E65-5B05-E611-9411-7427EA2F7F59', 'Content-Type': 'application/x-www-form-urlencoded'}

payload = {'Stream': 'saccoparking', 'SaccoName': 'Sacco 111',  
         'Vehicles': [
			{'VehicleType': 61, 'Duration': 1, 'RegistrationNumber': 'KBL690K'} ,
			{'VehicleType': 61, 'Duration': 1, 'RegistrationNumber': 'KBL690K'} 
		]

}

final = urlencode(payload)
print('Final ' + urllib.parse.unquote(final))

res = requests.post("http://197.254.58.150/jambopayservices/api/payments/POST", data=urllib.parse.unquote(final), headers=headers)
print(res.request.body)
print(res.text)



