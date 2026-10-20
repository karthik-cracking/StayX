// SPDX-License-Identifier: GPL-3.0-only
// StayX modifications, 2026-10-21. See LICENSE and NOTICE.
import java.io.*;
import java.nio.file.*;
import java.util.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.immutable.instruction.*;
import com.android.tools.smali.dexlib2.immutable.reference.*;
import com.android.tools.smali.dexlib2.rewriter.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;

public class StayXBranding {
 public static void main(String[] args) throws Exception {
  String html=Files.readString(Path.of(args[1]));
  int[] edits={0};
  for(Path p:Files.list(Path.of(args[0])).filter(x->x.toString().endsWith(".dex")).toList()) {
   DexFile dex=DexFileFactory.loadDexFile(p.toFile(),Opcodes.getDefault());
   boolean found=dex.getClasses().stream().anyMatch(c->c.getType().equals("Lapp/morphe/extension/shared/settings/preference/about/MorpheAboutPreference;"));
   if(!found)continue;
   DexRewriter rw=new DexRewriter(new RewriterModule(){
    @Override public Rewriter<Method> getMethodRewriter(Rewriters r){return new MethodRewriter(r){
     @Override public Method rewrite(Method m){
      if(m.getDefiningClass().equals("Lapp/morphe/extension/shared/settings/preference/about/MorpheAboutPreference;") && m.getName().equals("createDialogHtml")){
       edits[0]++;
       var impl=new ImmutableMethodImplementation(4,List.of(
        new ImmutableInstruction31c(Opcode.CONST_STRING_JUMBO,0,new ImmutableStringReference(html)),
        new ImmutableInstruction11x(Opcode.RETURN_OBJECT,0)),List.of(),List.of());
       return new ImmutableMethod(m.getDefiningClass(),m.getName(),m.getParameters(),m.getReturnType(),m.getAccessFlags(),m.getAnnotations(),m.getHiddenApiRestrictions(),impl);
      }
      return super.rewrite(m);
     }
    };}
   });
   Path dest=p.resolveSibling(p.getFileName()+".new");
   DexPool.writeTo(dest.toString(),rw.getDexFileRewriter().rewrite(dex));
   Files.move(dest,p,StandardCopyOption.REPLACE_EXISTING);
   System.out.println("Rebranded About page in "+p);
  }
  if(edits[0]!=1)throw new IllegalStateException("Expected exactly one About renderer, found "+edits[0]);
 }
}
