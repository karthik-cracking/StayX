// SPDX-License-Identifier: GPL-3.0-only
// StayX compatibility customization, 2026-11-17. Preserve LICENSE and NOTICE.
// Restores the legacy Morphe early-return guard for the optional Cast context fetch.
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

class LegacyCastCompatibility {
 static final String FINGERPRINT = "Error fetching CastContext.";
 static boolean matches(Method method) {
  if(method.getImplementation()==null)return false;
  for(Instruction instruction:method.getImplementation().getInstructions()) {
   if(instruction instanceof ReferenceInstruction reference && reference.getReference() instanceof StringReference string && string.getString().equals(FINGERPRINT))return true;
  }
  return false;
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
  if(candidates.size()!=1)throw new IllegalStateException("Expected exactly one Cast context fingerprint method; found "+candidates.size());
  Method matched=candidates.getFirst();
  if(!matched.getReturnType().equals("V"))throw new IllegalStateException("Fingerprint method must return void: "+prototype(matched));
  final String target=prototype(matched);
  int[] rewritten={0};
  DexRewriter rewriter=new DexRewriter(new RewriterModule(){
   @Override public Rewriter<Method> getMethodRewriter(Rewriters rewriters){return new MethodRewriter(rewriters){
    @Override public Method rewrite(Method method){
     if(!prototype(method).equals(target))return super.rewrite(method);
     rewritten[0]++;
     var implementation=new ImmutableMethodImplementation(method.getImplementation().getRegisterCount(),
       List.of(new ImmutableInstruction10x(Opcode.RETURN_VOID)),List.of(),List.of());
     return new ImmutableMethod(method.getDefiningClass(),method.getName(),method.getParameters(),method.getReturnType(),
       method.getAccessFlags(),method.getAnnotations(),method.getHiddenApiRestrictions(),implementation);
    }
   };}
  });
  Path replacement=matchedPath.resolveSibling(matchedPath.getFileName()+".legacy-new");
  DexPool.writeTo(replacement.toString(),rewriter.getDexFileRewriter().rewrite(inputs.get(matchedPath)));
  if(rewritten[0]!=1)throw new IllegalStateException("Expected one rewritten method; found "+rewritten[0]);
  DexFile verified=DexFileFactory.loadDexFile(replacement.toFile(),Opcodes.getDefault());
  int verifiedCount=0;
  for(ClassDef type:verified.getClasses())for(Method method:type.getMethods())if(prototype(method).equals(target)){
   List<Instruction> instructions=new ArrayList<>();method.getImplementation().getInstructions().forEach(instructions::add);
   if(instructions.size()!=1||instructions.getFirst().getOpcode()!=Opcode.RETURN_VOID)throw new IllegalStateException("Guard did not verify");
   verifiedCount++;
  }
  if(verifiedCount!=1)throw new IllegalStateException("Rewritten method count mismatch");
  Files.move(replacement,matchedPath,StandardCopyOption.REPLACE_EXISTING);
  System.out.println("Matched and guarded: "+target);
  System.out.println("Modified DEX: "+matchedPath.getFileName());
  System.out.println("Verified methods rewritten: "+verifiedCount);
  System.out.println("Cast context initialization is skipped by this legacy compatibility variant.");
 }
}
