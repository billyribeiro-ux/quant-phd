const fs=require('fs');
const katex=require(process.argv[2]);
const notation=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));
const macros={};
for(const [k,v] of Object.entries(notation.macros)) macros[k]=v.tex;
let bad=0,total=0;
for(const f of process.argv.slice(4)){
  const s=fs.readFileSync(f,'utf8');
  const re=/\\\((.+?)\\\)|\\\[(.+?)\\\]/gs; let m;
  while((m=re.exec(s))){
    const tex=(m[1]??m[2]).replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
    total++;
    try{ katex.renderToString(tex,{displayMode:!!m[2],throwOnError:true,strict:'error',trust:false,macros:{...macros}}); }
    catch(e){ bad++; console.log(f.split('/').pop(), String(e.message).slice(0,160), '::', tex.slice(0,80)); }
  }
}
console.log('expressions',total,'failing',bad);
