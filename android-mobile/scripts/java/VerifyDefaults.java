// SPDX-License-Identifier: GPL-3.0-only
// Independent check of the values supplied to the two background-setting constructors.
import java.nio.file.*;
import java.util.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;

class VerifyDefaults {
 public static void main(String[] args) throws Exception {
  Map<String,String> expected=Map.of("morphe_remove_background_playback_restrictions","TRUE","morphe_shorts_disable_background_playback","FALSE");
  Map<String,String> observed=new TreeMap<>();
  for(Path path:Files.list(Path.of(args[0])).filter(p->p.toString().endsWith(".dex")).toList()) {
   DexFile dex=DexFileFactory.loadDexFile(path.toFile(),Opcodes.getDefault());
   for(ClassDef type:dex.getClasses()) {
    if(!type.getType().startsWith("Lapp/morphe/")||!type.getType().endsWith("Settings;"))continue;
    for(Method method:type.getMethods()) {
     if(!method.getName().equals("<clinit>")||method.getImplementation()==null)continue;
     List<Instruction> instructions=new ArrayList<>();method.getImplementation().getInstructions().forEach(instructions::add);
     String pending=null;
     for(int i=0;i<instructions.size();i++) {
      Instruction ins=instructions.get(i);
      if(ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof StringReference sr&&expected.containsKey(sr.getString()))pending=sr.getString();
      if(pending!=null&&ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof MethodReference mr&&mr.getName().equals("<init>")&&mr.getDefiningClass().endsWith("/BooleanSetting;")) {
       if(!(ins instanceof FiveRegisterInstruction registers))throw new IllegalStateException("Unexpected constructor format");
       int reg=registers.getRegisterE();String actual=null;
       for(int j=i-1;j>=Math.max(0,i-8);j--) {
        Instruction prior=instructions.get(j);
        if(prior.getOpcode()==Opcode.SGET_OBJECT&&prior instanceof OneRegisterInstruction one&&one.getRegisterA()==reg&&prior instanceof ReferenceInstruction ref&&ref.getReference() instanceof FieldReference field&&field.getDefiningClass().equals("Ljava/lang/Boolean;")){actual=field.getName();break;}
       }
       if(observed.put(pending,actual)!=null)throw new IllegalStateException("Duplicate setting "+pending);
       pending=null;
      }
     }
    }
   }
  }
  System.out.println(observed);
  if(!observed.equals(expected))throw new IllegalStateException("Background defaults mismatch");
  System.out.println("Compiled DEX background defaults verified");
 }
}
