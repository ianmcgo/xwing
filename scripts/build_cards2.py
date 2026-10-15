import json,glob,re,sys,os

repo,out=sys.argv[1:3]

def cost_of(c):
    if isinstance(c,dict):
        if "value" in c:
            return c["value"]
        if "values" in c:
            return list(c["values"].values())[0]
    return 0

def strip(t):
    return re.sub(r"<[^>]+>","",t or "")

def restr(rs):
    parts=[]
    for r in rs or []:
        if "factions" in r:
            parts.append("/".join(r["factions"]))
        elif "ships" in r:
            parts.append("ships: "+", ".join(r["ships"]))
        elif "sizes" in r:
            parts.append("size: "+", ".join(r["sizes"]))
        elif "keywords" in r:
            parts.append("keyword: "+", ".join(r["keywords"]))
        else:
            parts.append(",".join(r.keys()))
    return "; ".join(parts)

ships={}
pilots=[]
for f in sorted(glob.glob(repo+"/data/pilots/*/*.json")):
    d=json.load(open(f))
    fac=d.get("faction","")
    stats=[]
    for s in d.get("stats",[]):
        if s["type"]=="attack":
            stats.append("Attack "+str(s["value"])+" ("+s.get("arc","")+")")
        else:
            stats.append(s["type"].capitalize()+" "+str(s["value"]))
    acts=[a["type"]+("" if a.get("difficulty")=="White" else " ("+a.get("difficulty","")+")") for a in d.get("actions",[])]
    ships[d["name"]]=[d.get("size",""),stats,acts]
    for p in d["pilots"]:
        pilots.append([fac,d["name"],p["name"],p.get("caption",""),p.get("initiative",0),p.get("cost",0),p.get("loadout",-1),p.get("slots",[]),strip(p.get("ability","")),strip(p.get("text","")),p.get("limited",0),p.get("xws",""),p.get("image",""),1 if p.get("standard") else 0,1 if p.get("extended") else 0,d.get("xws","")])

upgrades=[]
for f in sorted(glob.glob(repo+"/data/upgrades/*.json")):
    for u in json.load(open(f)):
        s=u["sides"][0]
        txt=strip(s.get("ability") or s.get("text") or "")
        for extra in u["sides"][1:]:
            t2=strip(extra.get("ability") or "")
            if t2:
                txt+="\n\n"+(extra.get("title") or "Other side")+": "+t2
        ch=s.get("charges",{}).get("value") if isinstance(s.get("charges"),dict) else None
        upgrades.append([u["name"],s.get("slots",[]),cost_of(u.get("cost")),txt,restr(u.get("restrictions")),u.get("xws",""),u.get("limited",0),ch or 0,1 if u.get("standard") else 0,1 if u.get("extended") else 0,s.get("image","")])

json.dump({"ships":ships,"pilots":pilots,"upgrades":upgrades},open(out,"w"),ensure_ascii=False,separators=(",",":"))
print(len(ships),len(pilots),len(upgrades),os.path.getsize(out))
