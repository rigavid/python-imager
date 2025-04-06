CONTROL        = {## Control characters ##
    #Unknown    SPaCe       LeFT        UP          DoWN        ORiGin      FULL        TOP         TAB         Re-TaB
    "UNK":"00", "SPC":"01", "LFT":"02", "UPP":"03", "DWN":"04", "ORG":"05", "FUL":"06", "TOP":"07", "TAB":"08", "RTB":"09",
}; FORMAT      = {## Format characters ##
    #UnFormat   UnderLine   TopLine     OverLine    ITalic      BolD        Cnt-Italic  ThiN        VertMirror  HrztlMirror
    "UF": "20", "UL": "21", "TL": "22", "OL": "23", "IT": "24", "BD": "25", "CI": "26", "TN": "27", "VM": "28", "HM": "29",
    #BackGrnd   ForeGround  LineS
    "BG": "30", "FG": "31", "LS": "32"
}; DIACRITICS  = {## Diacritics ## Using char's unicode's table point
    # Grave acc. Acute acc.   Circumflex   Caron acc.   Double grave Double acute Diaeresis    Dot above    Breve acc.   Macron acc.
    "0300":"40", "0301":"41", "0302":"42", "030c":"43", "030f":"44", "030b":"45", "0308":"46", "0307":"47", "0306":"48", "0304":"49",
    # Tilde acc. Line above   Dbl line ab. Ring above   Hook above
    "0303":"50", "030d":"51", "030e":"52", "030a":"53", "0309":"54",
    # Cedilla    Ogonyek      Line below   Dot below    Diaeresis b.
    "0327":"60", "0328":"61", "0329":"62", "0323":"63", "0324":"64",
    # Comb. horn
    "031b":"80"
}; SYMBOLS     = {## Numbers and symbols ##
    "0": "A0", "1": "A1", "2": "A2", "3": "A3", "4": "A4", "5": "A5", "6": "A6", "7": "A7", "8": "A8", "9": "A9",
    ".": "B0", ",": "B1", ":": "B2", ";": "B3", "-": "B4", "_": "B5", "!": "B6", "?": "B7", "¡": "B8", "¿": "B9",
    "'": "C0", '"': "C1", "·": "C2", "$": "C3", "%": "C4", "&": "C5", "/": "C6", "=": "C7", "+": "C8", "*": "C9",
    "(": "D0", ")": "D1", "[": "D2", "]": "D3", "{": "D4", "}": "D5", "|": "D6", "@": "D7", "#": "D8", "¬": "D9",
    "º": "E0", "ª": "E1", "`": "E2", "´": "E3", "^": "E4", "¨": "E5", "~": "E6", "€": "E7", "¢": "E8", "¶": "E9",
    "<": "F0", ">": "F1","\\": "F2", "£": "F3", "™": "F4", "±": "F5", "¦": "F6", "©": "F7", "×": "F8", "÷": "F9",
    "’": "G0", "«": "G1", "»": "G2",
}; latin_c     = {## Latin capitals ##
    "A":"A00", "B":"A01", "C":"A02", "D":"A03", "E":"A04", "F":"A05", "G":"A06", "H":"A07", "I":"A08", "J":"A09",
    "K":"A10", "L":"A11", "M":"A12", "N":"A13", "O":"A14", "P":"A15", "Q":"A16", "R":"A17", "S":"A18", "T":"A19",
    "U":"A20", "V":"A21", "W":"A22", "X":"A23", "Y":"A24", "Z":"A25", "Æ":"A26", "Œ":"A27", "Þ":"A28", "Ð":"A29",
}; cyrillic_c  = {## Cyrillic capitals ##
    "А":"A30", "Б":"A31", "В":"A32", "Г":"A33", "Д":"A34", "Е":"A35", "Ё":"A36", "Ж":"A37", "З":"A38", "И":"A39",
    "Й":"A40", "К":"A41", "Л":"A42", "М":"A43", "Н":"A44", "О":"A45", "П":"A46", "Р":"A47", "С":"A48", "Т":"A49",
    "У":"A50", "Ф":"A51", "Х":"A52", "Ц":"A53", "Ч":"A54", "Ш":"A55", "Щ":"A56", "Ъ":"A57", "Ы":"A58", "Ь":"A59",
    "Э":"A60", "Ю":"A61", "Я":"A62"
}; greek_c     = {## Greek capitals ##
    "Α":"A70", "Β":"A71", "Γ":"A72", "Δ":"A73", "Ε":"A74", "Ζ":"A75", "Η":"A76", "Θ":"A77", "Ι":"A78", "Κ":"A79",
    "Λ":"A80", "Μ":"A81", "Ν":"A82", "Ξ":"A83", "Ο":"A84", "Π":"A85", "Ρ":"A86", "Σ":"A87", "Ʃ":"A88", "Τ":"A89",
    "Υ":"A90", "Φ":"A91", "Χ":"A92", "Ψ":"A93", "Ω":"A94"
}; archaic_g_c = {## Archaic greek capitals ##
    "Ϙ":"A95", "Ϡ":"A96", "Ͳ":"A97",
}; latin_l     = {## latin lowercase ##
    "a":"B00", "b":"B01", "c":"B02", "d":"B03", "e":"B04", "f":"B05", "g":"B06", "h":"B07", "i":"B08", "j":"B09",
    "k":"B10", "l":"B11", "m":"B12", "n":"B13", "o":"B14", "p":"B15", "q":"B16", "r":"B17", "s":"B18", "t":"B19",
    "u":"B20", "v":"B21", "w":"B22", "x":"B23", "y":"B24", "z":"B25", "æ":"B26", "œ":"B27", "þ":"B28", "ð":"B29",
}; cyrillic_l  = {## cyrillic lowercase ##
    "а":"B30", "б":"B31", "в":"B32", "г":"B33", "д":"B34", "е":"B35", "ё":"B36", "ж":"B37", "з":"B38", "и":"B39",
    "й":"B40", "к":"B41", "л":"B42", "м":"B43", "н":"B44", "о":"B45", "п":"B46", "р":"B47", "с":"B48", "т":"B49",
    "у":"B50", "ф":"B51", "х":"B52", "ц":"B53", "ч":"B54", "ш":"B55", "щ":"B56", "ъ":"B57", "ы":"B58", "ь":"B59",
    "э":"B60", "ю":"B61", "я":"B62"
}; greek_l     = {## greek lowercase ##
    "α":"B70", "β":"B71", "γ":"B72", "δ":"B73", "ε":"B74", "ζ":"B75", "η":"B76", "θ":"B77", "ι":"B78", "κ":"B79",
    "λ":"B80", "μ":"B81", "ν":"B82", "ξ":"B83", "ο":"B84", "π":"B85", "ρ":"B86", "σ":"B87", "ς":"B88", "τ":"B89",
    "υ":"B90", "φ":"B91", "χ":"B92", "ψ":"B93", "ω":"B94"
}; archaic_g_l = {## archaic greek lowercase ##
    "ϙ":"B95", "ϡ":"B96", "ͳ":"B97"
}; greek_other = {## other greek lowercase ##
    "ϵ":"A98", "϶":"A99", "ϑ":"B98", "ϐ":"B99"
}; VIETNAMIESE = {## vietnamiese letters ##
    "Đ":"A63", "đ":"B63"
}; HEBREW      = {## Hebrew abjad ##
    "א":"C00", "ב":"C01", "ג":"C02", "ד":"C03", "ה":"C04", "ו":"C05", "ז":"C06", "ח":"C07", "ט":"C08", "י":"C09",
    "כ":"C10", "ך":"C11", "ל":"C12", "מ":"C13", "ם":"C14", "נ":"C15", "ן":"C16", "ס":"C17", "ע":"C18", "פ":"C19",
    "ף":"C20", "צ":"C21", "ץ":"C22", "ק":"C23", "ר":"C24", "ש":"C25", "ת":"C26", "בּ":"C27", "גּ":"C28", "דּ":"C29",
    "כּ":"C30", "ךּ":"C31", "פּ":"C32", "ףּ":"C33", "שׁ":"C34", "שׂ":"C35", "תּ":"C36", "ו":"C37", "וּ":"C38", "וֹ":"C39",
}
## Scripts to be added:
### Japanese
### Armenian
### Georgian
### Sitelen pona # cf. https://www.kreativekorp.com/ucsur/charts/sitelen.html

GREEK_ = archaic_g_c|archaic_g_l|greek_other
LATIN, CYRILLIC, GREEK = latin_c|latin_l, cyrillic_c|cyrillic_l, greek_c|greek_l
TEXT = SYMBOLS|LATIN|CYRILLIC|GREEK|GREEK_|VIETNAMIESE|HEBREW
CONV = CONTROL|FORMAT|DIACRITICS|TEXT
CHARS = {CONV[k] for k in CONV}
if __name__ == "__main__":
    used, total = len(CHARS), 100 + 26*10 + 26*100 # (0-99)+(A0-A9)+(A00-Z99)
    print(f"{used:0>4}/{total} => {used/total:.2%} used")
print("For (un) assigned codepoints cf. CODEPOINTS.md")