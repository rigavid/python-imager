CONTROL       = {## Control characters ##
    #Unknown    SPaCe       LeFT        UP          DoWN        ORiGin      FULL        TOP         TAB         Re-TaB
    "UNK":"00", "SPC":"01", "LFT":"02", "UPP":"03", "DWN":"04", "ORG":"05", "FUL":"06", "TOP":"07", "TAB":"08", "RTB":"09",
    #"   ":"10", "   ":"11", "   ":"12", "   ":"13", "   ":"14", "   ":"15", "   ":"16", "   ":"17", "   ":"18", "   ":"19",
}; FORMAT     = {## Format characters ##
    #UnFormat  UnderLine  TopLine    OverLine   ITalic     BolD       Cnt-Italic ThiN       VertMirror HrztlMirror
    "UF":"20", "UL":"21", "TL":"22", "OL":"23", "IT":"24", "BD":"25", "CI":"26", "TN":"27", "VM":"28", "HM":"29",
    #BackGrnd  ForeGround LineS
    "BG":"30", "FG":"31", "LS":"32",#"  ":"33", "  ":"34", "  ":"35", "  ":"36", "  ":"37", "  ":"38", "  ":"39",
}; DIACRITICS = {### Diacritics ##
    # As they are combining chars, I use here the hex value of the unicode table point
    # Grave acc. Acute acc.   Circumflex   Caron acc.   Double grave Double acute Diaeresis    Dot above    Breve acc.   Macron acc.
    "0300":"40", "0301":"41", "0302":"42", "030c":"43", "030f":"44", "030b":"45", "0308":"46", "0307":"47", "0306":"48", "0304":"49",
    # Tilde acc. Line above   Dbl line ab. Ring above
    "0303":"50", "030d":"51", "030e":"52", "030a":"53", "    ":"54", "    ":"55", "    ":"56", "    ":"57", "    ":"58", "    ":"59",
    #### Souscrit ##
    # Cedilla    Ogonyek      Line below   Dot below    Diaeresis b.
    "0327":"60", "0328":"61", "0329":"62", "0323":"63", "0324":"64", "    ":"65", "    ":"66", "    ":"67", "    ":"68", "    ":"69",
    "    ":"70", "    ":"71", "    ":"72", "    ":"73", "    ":"74", "    ":"75", "    ":"76", "    ":"77", "    ":"78", "    ":"79",
    #### Inscrit ##
    " ":"80", " ":"81", " ":"82", " ":"83", " ":"84", " ":"85", " ":"86", " ":"87", " ":"88", " ":"89",
    " ":"90", " ":"91", " ":"92", " ":"93", " ":"94", " ":"95", " ":"96", " ":"97", " ":"98", " ":"99",
}; SYMBOLS    = {#### Numbers and symbols ##
    "0":"A0", "1":"A1", "2":"A2", "3":"A3", "4":"A4", "5":"A5", "6":"A6", "7":"A7", "8":"A8", "9":"A9",
    ".":"B0", ",":"B1", ":":"B2", ";":"B3", "-":"B4", "_":"B5", "!":"B6", "?":"B7", "¡":"B8", "¿":"B9",
    "'":"C0", '"':"C1", "·":"C2", "$":"C3", "%":"C4", "&":"C5", "/":"C6", "=":"C7", "+":"C8", "*":"C9",
    "(":"D0", ")":"D1", "[":"D2", "]":"D3", "{":"D4", "}":"D5", "|":"D6", "@":"D7", "#":"D8", "¬":"D9",
    "º":"E0", "ª":"E1", "`":"E2", "´":"E3", "^":"E4", "¨":"E5", "~":"E6", "€":"E7", "¢":"E8", "¶":"E9",
    "<":"F0", ">":"F1","\\":"F2", "£":"F3", "™":"F4", "±":"F5", "¦":"F6", "©":"F7", "×":"F8", "÷":"F9",
    "’":"G0", "«":"G1", "»":"G2",#" ":"G3", " ":"G4", " ":"G5", " ":"G6", " ":"G7", " ":"G8", " ":"G9",
    #" ":"H0", " ":"H1", " ":"H2", " ":"H3", " ":"H4", " ":"H5", " ":"H6", " ":"H7", " ":"H8", " ":"H9",
    #" ":"I0", " ":"I1", " ":"I2", " ":"I3", " ":"I4", " ":"I5", " ":"I6", " ":"I7", " ":"I8", " ":"I9",
    #" ":"J0", " ":"J1", " ":"J2", " ":"J3", " ":"J4", " ":"J5", " ":"J6", " ":"J7", " ":"J8", " ":"J9",
    #" ":"K0", " ":"K1", " ":"K2", " ":"K3", " ":"K4", " ":"K5", " ":"K6", " ":"K7", " ":"K8", " ":"K9",
    #" ":"L0", " ":"L1", " ":"L2", " ":"L3", " ":"L4", " ":"L5", " ":"L6", " ":"L7", " ":"L8", " ":"L9",
    #" ":"M0", " ":"M1", " ":"M2", " ":"M3", " ":"M4", " ":"M5", " ":"M6", " ":"M7", " ":"M8", " ":"M9",
    #" ":"N0", " ":"N1", " ":"N2", " ":"N3", " ":"N4", " ":"N5", " ":"N6", " ":"N7", " ":"N8", " ":"N9",
    #" ":"O0", " ":"O1", " ":"O2", " ":"O3", " ":"O4", " ":"O5", " ":"O6", " ":"O7", " ":"O8", " ":"O9",
    #" ":"P0", " ":"P1", " ":"P2", " ":"P3", " ":"P4", " ":"P5", " ":"P6", " ":"P7", " ":"P8", " ":"P9",
    #" ":"Q0", " ":"Q1", " ":"Q2", " ":"Q3", " ":"Q4", " ":"Q5", " ":"Q6", " ":"Q7", " ":"Q8", " ":"Q9",
    #" ":"R0", " ":"R1", " ":"R2", " ":"R3", " ":"R4", " ":"R5", " ":"R6", " ":"R7", " ":"R8", " ":"R9",
    #" ":"S0", " ":"S1", " ":"S2", " ":"S3", " ":"S4", " ":"S5", " ":"S6", " ":"S7", " ":"S8", " ":"S9",
    #" ":"T0", " ":"T1", " ":"T2", " ":"T3", " ":"T4", " ":"T5", " ":"T6", " ":"T7", " ":"T8", " ":"T9",
    #" ":"U0", " ":"U1", " ":"U2", " ":"U3", " ":"U4", " ":"U5", " ":"U6", " ":"U7", " ":"U8", " ":"U9",
    #" ":"V0", " ":"V1", " ":"V2", " ":"V3", " ":"V4", " ":"V5", " ":"V6", " ":"V7", " ":"V8", " ":"V9",
    #" ":"W0", " ":"W1", " ":"W2", " ":"W3", " ":"W4", " ":"W5", " ":"W6", " ":"W7", " ":"W8", " ":"W9",
    #" ":"X0", " ":"X1", " ":"X2", " ":"X3", " ":"X4", " ":"X5", " ":"X6", " ":"X7", " ":"X8", " ":"X9",
    #" ":"Y0", " ":"Y1", " ":"Y2", " ":"Y3", " ":"Y4", " ":"Y5", " ":"Y6", " ":"Y7", " ":"Y8", " ":"Y9",
    #" ":"Z0", " ":"Z1", " ":"Z2", " ":"Z3", " ":"Z4", " ":"Z5", " ":"Z6", " ":"Z7", " ":"Z8", " ":"Z9",
}; latin_c    = {## Latin capitals ##
    "A":"A00", "B":"A01", "C":"A02", "D":"A03", "E":"A04", "F":"A05", "G":"A06", "H":"A07", "I":"A08", "J":"A09",
    "K":"A10", "L":"A11", "M":"A12", "N":"A13", "O":"A14", "P":"A15", "Q":"A16", "R":"A17", "S":"A18", "T":"A19",
    "U":"A20", "V":"A21", "W":"A22", "X":"A23", "Y":"A24", "Z":"A25", "Æ":"A26", "Œ":"A27", "Þ":"A28", "Ð":"A29",
}; cyrillic_c = {## Cyrillic capitals ##
    "А":"A30", "Б":"A31", "В":"A32", "Г":"A33", "Д":"A34", "Е":"A35", "Ё":"A36", "Ж":"A37", "З":"A38", "И":"A39",
    "Й":"A40", "К":"A41", "Л":"A42", "М":"A43", "Н":"A44", "О":"A45", "П":"A46", "Р":"A47", "С":"A48", "Т":"A49",
    "У":"A50", "Ф":"A51", "Х":"A52", "Ц":"A53", "Ч":"A54", "Ш":"A55", "Щ":"A56", "Ъ":"A57", "Ы":"A58", "Ь":"A59",
    "Э":"A60", "Ю":"A61", "Я":"A62",#" ":"A63", " ":"A64", " ":"A65", " ":"A66", " ":"A67", " ":"A68", " ":"A69",
}; greek_c    = {## Greek capitals ##
    "Α":"A70", "Β":"A71", "Γ":"A72", "Δ":"A73", "Ε":"A74", "Ζ":"A75", "Η":"A76", "Θ":"A77", "Ι":"A78", "Κ":"A79",
    "Λ":"A80", "Μ":"A81", "Ν":"A82", "Ξ":"A83", "Ο":"A84", "Π":"A85", "Ρ":"A86", "Σ":"A87", "Ʃ":"A88", "Τ":"A89",
    "Υ":"A90", "Φ":"A91", "Χ":"A92", "Ψ":"A93", "Ω":"A94", "Ϙ":"A95", "Ϡ":"A96", "Ͳ":"A97", "ϵ":"A98", "϶":"A99",
}; latin_l    = {## latin lowercase ##
    "a":"B00", "b":"B01", "c":"B02", "d":"B03", "e":"B04", "f":"B05", "g":"B06", "h":"B07", "i":"B08", "j":"B09",
    "k":"B10", "l":"B11", "m":"B12", "n":"B13", "o":"B14", "p":"B15", "q":"B16", "r":"B17", "s":"B18", "t":"B19",
    "u":"B20", "v":"B21", "w":"B22", "x":"B23", "y":"B24", "z":"B25", "æ":"B26", "œ":"B27", "þ":"B28", "ð":"B29",
}; cyrillic_l = {## cyrillic lowercase ##
    "а":"B30", "б":"B31", "в":"B32", "г":"B33", "д":"B34", "е":"B35", "ё":"B36", "ж":"B37", "з":"B38", "и":"B39",
    "й":"B40", "к":"B41", "л":"B42", "м":"B43", "н":"B44", "о":"B45", "п":"B46", "р":"B47", "с":"B48", "т":"B49",
    "у":"B50", "ф":"B51", "х":"B52", "ц":"B53", "ч":"B54", "ш":"B55", "щ":"B56", "ъ":"B57", "ы":"B58", "ь":"B59",
    "э":"B60", "ю":"B61", "я":"B62",#" ":"B63", " ":"B64", " ":"B65", " ":"B66", " ":"B67", " ":"B68", " ":"B69",
}; greek_l    = {## greek lowercase ##
    "α":"B70", "β":"B71", "γ":"B72", "δ":"B73", "ε":"B74", "ζ":"B75", "η":"B76", "θ":"B77", "ι":"B78", "κ":"B79",
    "λ":"B80", "μ":"B81", "ν":"B82", "ξ":"B83", "ο":"B84", "π":"B85", "ρ":"B86", "σ":"B87", "ς":"B88", "τ":"B89",
    "υ":"B90", "φ":"B91", "χ":"B92", "ψ":"B93", "ω":"B94", "ϙ":"B95", "ϡ":"B96", "ͳ":"B97", "ϑ":"B98", "ϐ":"B99",
}
## Scripts to be added:
### Japanese
### Armenian
### Georgian
### Hebrew
### Vietnamiese

# {
#     "":"C00", "":"C01", "":"C02", "":"C03", "":"C04", "":"C05", "":"C06", "":"C07", "":"C08", "":"C09",
#     "":"C10", "":"C11", "":"C12", "":"C13", "":"C14", "":"C15", "":"C16", "":"C17", "":"C18", "":"C19",
#     "":"C20", "":"C21", "":"C22", "":"C23", "":"C24", "":"C25", "":"C26", "":"C27", "":"C28", "":"C29",
#     "":"C30", "":"C31", "":"C32", "":"C33", "":"C34", "":"C35", "":"C36", "":"C37", "":"C38", "":"C39",
#     "":"C40", "":"C41", "":"C42", "":"C43", "":"C44", "":"C45", "":"C46", "":"C47", "":"C48", "":"C49",
#     "":"C50", "":"C51", "":"C52", "":"C53", "":"C54", "":"C55", "":"C56", "":"C57", "":"C58", "":"C59",
#     "":"C60", "":"C61", "":"C62", "":"C63", "":"C64", "":"C65", "":"C66", "":"C67", "":"C68", "":"C69",
#     "":"C70", "":"C71", "":"C72", "":"C73", "":"C74", "":"C75", "":"C76", "":"C77", "":"C78", "":"C79",
#     "":"C80", "":"C81", "":"C82", "":"C83", "":"C84", "":"C85", "":"C86", "":"C87", "":"C88", "":"C89",
#     "":"C90", "":"C91", "":"C92", "":"C93", "":"C94", "":"C95", "":"C96", "":"C97", "":"C98", "":"C99",
# }

LATIN, CYRILLIC, GREEK = latin_c|latin_l, cyrillic_c|cyrillic_l, greek_c|greek_l
TEXT = SYMBOLS|LATIN|CYRILLIC|GREEK
CONV = CONTROL|FORMAT|DIACRITICS|TEXT
for i in [" "*n for n in range(5)]:
    try: del CONV[i]
    except: pass
CHARS = [CONV[k] for k in CONV]
if __name__ == "__main__":
    used, total = len(CHARS), 100 + 26*10 + 26*100 # (0-99)+(A0-A9)+(A00-Z99)
    print(f"{used:0>4}/{total} => {used/total:.2%} used")