// SPDX-License-Identifier: GPL-3.0-only
// StayX modifications, 2026-10-21. See LICENSE and NOTICE.
import java.nio.file.*;import java.util.*;
import com.android.tools.smali.dexlib2.*;import com.android.tools.smali.dexlib2.iface.*;import com.android.tools.smali.dexlib2.iface.instruction.*;import com.android.tools.smali.dexlib2.iface.reference.*;
import com.android.tools.smali.dexlib2.immutable.*;import com.android.tools.smali.dexlib2.immutable.reference.*;import com.android.tools.smali.dexlib2.rewriter.*;import com.android.tools.smali.dexlib2.writer.pool.DexPool;
import com.android.tools.smali.dexlib2.builder.*;import com.android.tools.smali.dexlib2.builder.instruction.*;
class OptionalDefaults {
 public static void main(String[] a)throws Exception{
  Set<String> off=new HashSet<>(Files.readAllLines(Path.of(a[1])));
  Map<String,String> colors=Map.of("morphe_theme_color_dark_custom","#080810","morphe_seekbar_custom_color_primary","#00D7FF","morphe_seekbar_custom_color_accent","#A83BFF");
  int[] total={0};
  for(Path p:Files.list(Path.of(a[0])).filter(x->x.toString().endsWith(".dex")).toList()){
   var d=DexFileFactory.loadDexFile(p.toFile(),Opcodes.getDefault());
   if(d.getClasses().stream().noneMatch(c->c.getType().startsWith("Lapp/morphe/")&&c.getType().endsWith("Settings;")))continue;
   int before=total[0];
   var rw=new DexRewriter(new RewriterModule(){public Rewriter<Method> getMethodRewriter(Rewriters r){return new MethodRewriter(r){public Method rewrite(Method m){
    if(!m.getDefiningClass().startsWith("Lapp/morphe/")||!m.getDefiningClass().endsWith("Settings;")||!m.getName().equals("<clinit>"))return super.rewrite(m);
    var orig=m.getImplementation();if(orig==null)return m;
    var ins=new ArrayList<Instruction>();orig.getInstructions().forEach(ins::add);
    record Change(int index,int reg,String key,boolean bool){}
    var changes=new ArrayList<Change>();String pending=null;
    for(int i=0;i<ins.size();i++){
     var in=ins.get(i);
     if(in instanceof ReferenceInstruction ri && ri.getReference() instanceof StringReference sr && (off.contains(sr.getString())||colors.containsKey(sr.getString())))pending=sr.getString();
     if(pending!=null && in instanceof ReferenceInstruction ri && ri.getReference() instanceof MethodReference mr && mr.getName().equals("<init>") && (mr.getDefiningClass().endsWith("/BooleanSetting;")||mr.getDefiningClass().endsWith("/StringSetting;"))){
      if(!(in instanceof FiveRegisterInstruction regs))throw new IllegalStateException("Unexpected setting constructor format");
      boolean bool=mr.getDefiningClass().endsWith("/BooleanSetting;");
      if((bool&&off.contains(pending))||(!bool&&colors.containsKey(pending)))changes.add(new Change(i,regs.getRegisterE(),pending,bool));
      pending=null;
     }
    }
    if(changes.isEmpty())return m;
    int scratch=orig.getRegisterCount();var impl=new MutableMethodImplementation(orig);
    Collections.reverse(changes);
    for(var c:changes){
     int i=c.index(),v=c.reg();
     impl.addInstruction(i+1,new BuilderInstruction32x(Opcode.MOVE_OBJECT_16,v,scratch));
     impl.addInstruction(i,new BuilderInstruction32x(Opcode.MOVE_OBJECT_16,scratch,v));
     if(c.bool())impl.addInstruction(i+1,new BuilderInstruction21c(Opcode.SGET_OBJECT,v,new ImmutableFieldReference("Ljava/lang/Boolean;",c.key().equals("morphe_shorts_disable_background_playback")?"TRUE":"FALSE","Ljava/lang/Boolean;")));
     else impl.addInstruction(i+1,new BuilderInstruction31c(Opcode.CONST_STRING_JUMBO,v,new ImmutableStringReference(colors.get(c.key()))));
     total[0]++;System.out.println("Default "+c.key()+" = "+(c.bool()?"off":colors.get(c.key())));
    }
    return new ImmutableMethod(m.getDefiningClass(),m.getName(),m.getParameters(),m.getReturnType(),m.getAccessFlags(),m.getAnnotations(),m.getHiddenApiRestrictions(),new ImmutableMethodImplementation(scratch+1,impl.getInstructions(),impl.getTryBlocks(),impl.getDebugItems()));
   }};}});
   Path n=p.resolveSibling(p.getFileName()+".new");DexPool.writeTo(n.toString(),rw.getDexFileRewriter().rewrite(d));Files.move(n,p,StandardCopyOption.REPLACE_EXISTING);
  }
  System.out.println("Updated defaults: "+total[0]);if(total[0]<5)throw new IllegalStateException("Too few defaults patched");
 }
}
