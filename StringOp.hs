{-
string operation
-}

module StringOp
( 
   sSplitHead,
   fCheck,
   sCheck,
   sSkip,
   spaceSkip
) where 

import qualified Data.Strings as S

type P a = a -> (a, a)

sSplitHead :: String -> P String
sSplitHead "" t = ("", t)
sSplitHead s t = if S.sStartsWith t s then (s, drop (length s) t) else ("", "")

fCheck :: (Char -> Bool) -> P String
fCheck f "" = ("", "")
fCheck f (c:s) = let (p, r) = (fCheck f s) in (if (f c) then (c:p, r) else ("", c:s))

sCheck :: String -> P String
sCheck t = fCheck (`elem` t)

sSkip :: String -> String -> String
sSkip t = dropWhile (`elem` t)

spaceSkip :: String -> String
spaceSkip = sSkip " \t\n"

main = do
   putStrLn (sSkip "T " " The factorial of 5 is:")
