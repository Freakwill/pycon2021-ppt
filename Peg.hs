module Peg
(
    ParseExpression
)
where

import Data.Monoid
import Data.Semigroup
import StringOp


data ParseElement = Literal String | Word String String | Enhance ParseElement
data ParseResults = String | List ParseResults
data ParseExpression = ParseElement | Add [ParseExpression] | Optional ParseExpression | ZeroOrMore ParseExpression | OneOrMore ParseExpression


class Parser a where
    preprocess :: String -> String
    parseImpl :: a -> String -> (ParseResults, String)
    parse :: a -> String -> (ParseResults, String)
    parse a s = parseImpl a (preprocess s)

instance Semigroup ParseExpression where
    pe <> pe1 = Add [pe, pe1]

instance Parser ParseExpression where
    preprocess :: String -> String
    preprocess = spaceSkip

    parseImpl :: ParseExpression -> String -> (ParseResults, String)
    parseImpl pe "" = ([], "")
    parseImpl (Literal t) s = let (result, rest) = sSplitHead t s in (if result /= [] then ([t], rest) else ([], ""))
    parseImpl (Word t1 t2) (c:s) = let (result, rest) = (sCheck t2 s) in (if c `elem` t1 then (c:result, rest) else ([], ""))
    parseImpl (Add []) s = ([], s)
    parseImpl (Add pe:pelist) s = let (result, rest) = (parse pe s) in if result /= "" then (result:result1, rest1) else ([],"")
        where (result:result1, rest1) = (parse pelist s)
    parseImpl (Optional pe) s = let (result, rest) = (parse pe s) in if result == "" then ("", s) else (result, rest)
    parseImpl (ZeroOrMore pe) s = let (result, rest) = (parse pe s) in if result == "" then ("", s) else parse (ZeroOrMore pe) s
    parseImpl (OneOrMore pe) s = let (result, rest) = (parse pe s) in if result == "" then ("", "") else parse (ZeroOrMore pe) s


main :: IO ()
main = do 
   print (sCheck "hello" "helloworld") 
