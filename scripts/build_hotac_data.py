import json,re,sys

repo,out=sys.argv[1:3]
files=["astromech","cannon","configuration","crew","device","force-power","gunner","illicit","missile","modification","sensor","talent","tech","title","torpedo","turret"]
cards=[]
for f in files:
    for u in json.load(open(repo+"/data/upgrades/"+f+".json")):
        s=u["sides"][0]
        slots=["Payload" if x=="Device" else x for x in s.get("slots",[])]
        fac=[];ships=[];sizes=[];other=[]
        for r in u.get("restrictions",[]):
            if "factions" in r:
                fac+=r["factions"]
            elif "ships" in r:
                ships+=r["ships"]
            elif "sizes" in r:
                sizes+=r["sizes"]
            else:
                other.append(",".join(k for k in r))
        if fac and "rebelalliance" not in fac:
            continue
        c=u.get("cost")
        if isinstance(c,dict):
            v=c.get("value")
            if v is None and "values" in c:
                v=list(c["values"].values())[0]
        else:
            v=None
        text=s.get("ability") or s.get("text") or ""
        text=re.sub(r"<[^>]+>","",text)
        cards.append([u["name"],slots,v or 0,text,ships,[x.lower() for x in sizes],",".join(other),s.get("image",""),1 if u.get("standard") else 0])
json.dump(cards,open(out,"w"),ensure_ascii=False,separators=(",",":"))
print(len(cards))
