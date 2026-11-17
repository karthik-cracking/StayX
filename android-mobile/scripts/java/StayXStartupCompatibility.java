// SPDX-License-Identifier: GPL-3.0-only
// StayX compatibility customization, 2026-11-17. Preserve LICENSE and NOTICE.
// Routes startup through the existing Lottie player so StayX branding works on Rive-capable releases.
import java.nio.file.*;
import java.util.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.immutable.instruction.*;
import com.android.tools.smali.dexlib2.rewriter.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;

class StayXStartupCompatibility {
 static boolean matches(Method method) {
  return method.getImplementation()!=null && (
   (method.getDefiningClass().equals("Lapp/morphe/extension/shared/patches/SplashAnimationPatch;") && method.getName().equals("isRiveIncluded")) ||
   (method.getDefiningClass().equals("Lapp/morphe/extension/shared/patches/SplashAnimationPatch$SplashScreenAnimationStyle;") && method.getName().equals("isRive")));

 }
 static String prototype(Method method) {
  return method.getDefiningClass()+"->"+method.getName()+"("+String.join("",method.getParameterTypes())+")"+method.getReturnType();
 }
 public static void main(String[] args) throws Exception {
  if(args.length!=1)throw new IllegalArgumentException("Pass a directory containing copied DEX files");
  List<Path> paths=Files.list(Path.of(args[0])).filter(path->path.toString().endsWith(".dex")).sorted().toList();
  Map<Path,DexFile> inputs=new LinkedHashMap<>();
  List<Method> candidates=new ArrayList<>();
  Path matchedPath=null;
  for(Path path:paths) {
   DexFile dex=DexFileFactory.loadDexFile(path.toFile(),Opcodes.getDefault());
   inputs.put(path,dex);
   for(ClassDef type:dex.getClasses())for(Method method:type.getMethods())if(matches(method)){candidates.add(method);matchedPath=path;}
  }
  if(candidates.size()!=2)throw new IllegalStateException("Expected exactly two startup routing methods; found "+candidates.size());
  Method matched=candidates.getFirst();
  if(!matched.getReturnType().equals("Z"))throw new IllegalStateException("Startup method must return boolean: "+prototype(matched));
  final Set<String> targets=new HashSet<>(); for(Method candidate:candidates)targets.add(prototype(candidate)); final String target=targets.toString();
  int[] rewritten={0};
  DexRewriter rewriter=new DexRewriter(new RewriterModule(){
   @Override public Rewriter<Method> getMethodRewriter(Rewriters rewriters){return new MethodRewriter(rewriters){
    @Override public Method rewrite(Method method){
     if(!targets.contains(prototype(method)))return super.rewrite(method);
     rewritten[0]++;
     var implementation=new ImmutableMethodImplementation(method.getImplementation().getRegisterCount(),
       List.of(new ImmutableInstruction11n(Opcode.CONST_4,0,0), new ImmutableInstruction11x(Opcode.RETURN,0)),List.of(),List.of());
     return new ImmutableMethod(method.getDefiningClass(),method.getName(),method.getParameters(),method.getReturnType(),
       method.getAccessFlags(),method.getAnnotations(),method.getHiddenApiRestrictions(),implementation);
    }
   };}
  });
  for(Path currentPath:inputs.keySet()) {
  matchedPath=currentPath;
  int before=rewritten[0];
  Path replacement=matchedPath.resolveSibling(matchedPath.getFileName()+".legacy-new");
  DexPool.writeTo(replacement.toString(),rewriter.getDexFileRewriter().rewrite(inputs.get(matchedPath)));
  if(rewritten[0]==before){Files.delete(replacement);continue;}
  DexFile verified=DexFileFactory.loadDexFile(replacement.toFile(),Opcodes.getDefault());
  int verifiedCount=0;
  for(ClassDef type:verified.getClasses())for(Method method:type.getMethods())if(targets.contains(prototype(method))){
   List<Instruction> instructions=new ArrayList<>();method.getImplementation().getInstructions().forEach(instructions::add);
   if(instructions.size()!=2||instructions.getLast().getOpcode()!=Opcode.RETURN)throw new IllegalStateException("Guard did not verify");
   verifiedCount++;
  }
  if(verifiedCount!=rewritten[0]-before)throw new IllegalStateException("Rewritten method count mismatch");
  Files.move(replacement,matchedPath,StandardCopyOption.REPLACE_EXISTING);
  }
  if(rewritten[0]!=2)throw new IllegalStateException("Expected two startup guards");
  System.out.println("Matched and guarded: "+target);
  System.out.println("Modified DEX: "+matchedPath.getFileName());
  System.out.println("Verified methods rewritten: "+rewritten[0]);
  System.out.println("Rive is bypassed so the StayX Lottie resource is used.");
 }
}

