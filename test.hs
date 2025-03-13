-- Define the required data type
data Formula = Const Bool
    | Prop String
    | Not Formula
    | Or [Formula]
    | And [Formula]
    | Impl Formula Formula
    | Equiv Formula Formula
  

-- Custom Show instance to display formulas correctly
instance Show Formula where
    show (Const True) = "T"
    show (Const False) = "F"
    show (Prop x) = x
    show (Not f) = "~" ++ show f  -- ✅ Uses correct negation symbol
    show (And fs) = "(" ++ joinListWithChar " & " (map show fs) ++ ")"  -- ✅ Correctly joins AND elements
    show (Or fs) = "(" ++ joinListWithChar " | " (map show fs) ++ ")" 
    show (Impl f1 f2) = "(" ++ show f1 ++ " -> " ++ show f2 ++ ")"
    show (Equiv f1 f2) = "(" ++ show f1 ++ " <-> " ++ show f2 ++ ")"

-- Helper function to join elements with a separator (since no imports are allowed)
joinListWithChar :: String -> [String] -> String
joinListWithChar _ [] = ""      -- ✅ Empty list case
joinListWithChar _ [x] = x      -- ✅ Single element case (no separator needed)
joinListWithChar sep (x:xs) = x ++ sep ++ joinListWithChar sep xs 

--Method to obtain 
toNNF :: Formula -> Formula
toNNF (Const b) = Const b
toNNF (Prop x) = Prop x
toNNF (Impl f1 f2) = toNNF (Or [Not f1, f2])  -- ✅ Fixed capitalization
toNNF f = f 



-- Main function to test output
main :: IO ()
main = do
    --putStrLn (show (Const True))   -- ✅ Should print "T"
    --putStrLn (show (Const False))  -- ✅ Should print "F"
    --putStrLn (show (Not (Prop "p")))  -- ✅ Should print "∼p"
    --putStrLn (show (And [Prop "p", Prop "q", Prop "r"]))
    let implFormula = Impl (Prop "p") (Prop "q")
    let equivFormula = Equiv (Const True) (Const True)
    let negatedOr = (Or [Prop "p", Prop "q"])  -- ∼(p | q)
    let checkInstance = Equiv (Prop "q") (Or[Const False, Not(Prop "r")])
    --print negatedOr
    
    putStrLn "\nBefore to NNF:"
    print implFormula 
    --print equivFormula
    --print checkInstance

    putStrLn "\nConverted to NNF:"
    print (toNNF implFormula)


