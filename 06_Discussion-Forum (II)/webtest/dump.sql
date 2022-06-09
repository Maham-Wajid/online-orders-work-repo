BEGIN TRANSACTION;
CREATE TABLE claim (
    claimID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,   -- CLaim ID number
    topic INTEGER NOT NULL REFERENCES topic(topicID) ON DELETE CASCADE ON UPDATE CASCADE, -- FK of claim
    postingUser INTEGER REFERENCES user(userID) ON DELETE SET NULL ON UPDATE CASCADE, -- FK of poisting user

   text TEXT NOT NULL,
    creationTime datetime NOT NULL,   -- Time topic was created
    updateTime datetime NOT NULL                         -- Last time a reply was added
                                  -- Actual text
);
INSERT INTO "claim" VALUES(5,11,4,'Claim 1 to topic 2','2022-04-24','2022-04-24');
INSERT INTO "claim" VALUES(6,13,4,'Claim to topic 3','2022-04-24','2022-04-24');
CREATE TABLE claimToClaim (
    claimRelID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                        -- Claim relationship ID
    first INTEGER NOT NULL REFERENCES claim(claimID) ON DELETE CASCADE ON UPDATE CASCADE, -- FK of first related claim
    second INTEGER NOT NULL REFERENCES claim(claimID) ON DELETE CASCADE ON UPDATE CASCADE, -- FK of second related claim
    claimRelType INTEGER NOT NULL REFERENCES claimToClaimType(claimRelTypeID) ON DELETE CASCADE ON UPDATE CASCADE,
                                                                                            -- FK of type of relation
    /* Specify that there can't be several relationships between the same pair of two claims */
    CONSTRAINT claimToClaimUnique UNIQUE (first, second)
);
CREATE TABLE claimToClaimType (
    claimRelTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    claimRelType TEXT NOT NULL
);
INSERT INTO "claimToClaimType" VALUES(1,'Opposed');
INSERT INTO "claimToClaimType" VALUES(2,'Equivalent');
CREATE TABLE replyText (
    replyTextID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                           -- Reply ID
    postingUser INTEGER REFERENCES user(userID) ON DELETE SET NULL ON UPDATE CASCADE, -- FK of posting user
    creationTime datetime NOT NULL,                                                    -- Posting time
    text TEXT NOT NULL                                                                -- Text of reply
);
INSERT INTO "replyText" VALUES(25,4,'2022-04-24','reply 1 to claim 1');
INSERT INTO "replyText" VALUES(26,4,'2022-04-24','reply 2 to claim 1');
INSERT INTO "replyText" VALUES(27,4,'2022-04-24','reply 3 to claim 1');
INSERT INTO "replyText" VALUES(28,4,'2022-04-24','reply 1 to claim reply 3');
INSERT INTO "replyText" VALUES(29,4,'2022-04-24','reply 2 to claim reply 3');
INSERT INTO "replyText" VALUES(30,4,'2022-04-24','reply 3 to claim reply 3');
CREATE TABLE replyToClaim (
    replyToClaimID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                                       -- Relationship ID
    reply INTEGER NOT NULL REFERENCES replyText (replyTextID) ON DELETE CASCADE ON UPDATE CASCADE,   -- FK of related reply
    claim INTEGER NOT NULL REFERENCES claim (claimID) ON DELETE CASCADE ON UPDATE CASCADE,           -- FK of related claim
    replyToClaimRelType INTEGER NOT NULL REFERENCES replyToClaimType(claimReplyTypeID) ON DELETE CASCADE ON UPDATE CASCADE -- FK of relation type
);
INSERT INTO "replyToClaim" VALUES(21,25,5,1);
INSERT INTO "replyToClaim" VALUES(22,26,5,2);
INSERT INTO "replyToClaim" VALUES(23,27,5,3);
CREATE TABLE replyToClaimType (
    claimReplyTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    claimReplyType TEXT NOT NULL
);
INSERT INTO "replyToClaimType" VALUES(1,'Clarification');
INSERT INTO "replyToClaimType" VALUES(2,'Supporting Argument');
INSERT INTO "replyToClaimType" VALUES(3,'Counterargument');
CREATE TABLE replyToReply (
    replyToReplyID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                                         -- Relationship ID
    reply INTEGER NOT NULL REFERENCES replyText(replyTextID) ON DELETE CASCADE ON UPDATE CASCADE,
    parent INTEGER NOT NULL REFERENCES replyText(replyTextID) ON DELETE CASCADE ON UPDATE CASCADE,
    replyToReplyRelType INTEGER NOT NULL REFERENCES replyToReplyType(replyReplyTypeID) ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO "replyToReply" VALUES(5,28,27,1);
INSERT INTO "replyToReply" VALUES(6,29,27,2);
INSERT INTO "replyToReply" VALUES(7,30,27,3);
CREATE TABLE replyToReplyType (
    replyReplyTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    replyReplyType TEXT NOT NULL
);
INSERT INTO "replyToReplyType" VALUES(1,'Evidence');
INSERT INTO "replyToReplyType" VALUES(2,'Support');
INSERT INTO "replyToReplyType" VALUES(3,'Rebuttal');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('user',4);
INSERT INTO "sqlite_sequence" VALUES('claimToClaimType',2);
INSERT INTO "sqlite_sequence" VALUES('replyToClaimType',3);
INSERT INTO "sqlite_sequence" VALUES('replyToReplyType',3);
INSERT INTO "sqlite_sequence" VALUES('topic',13);
INSERT INTO "sqlite_sequence" VALUES('claim',6);
INSERT INTO "sqlite_sequence" VALUES('replyText',30);
INSERT INTO "sqlite_sequence" VALUES('replyToClaim',23);
INSERT INTO "sqlite_sequence" VALUES('replyToReply',7);
CREATE TABLE topic (
    topicID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,  -- Topic's ID number
    topicName TEXT NOT NULL,                             -- Topic's text
    postingUser INTEGER REFERENCES user(userID) ON DELETE SET NULL ON UPDATE CASCADE, -- FK (foreign key) of posting user
    creationTime datetime NOT NULL,                       -- Time topic was created
    updateTime datetime NOT NULL                          -- Last time a claim/reply was added
);
INSERT INTO "topic" VALUES(10,'Topic 1',4,'2022-04-24','2022-04-24');
INSERT INTO "topic" VALUES(11,'Topic 2',4,'2022-04-24','2022-04-24');
INSERT INTO "topic" VALUES(13,'topic 3',4,'2022-04-24','2022-04-24');
CREATE TABLE user (
    userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, -- Integer user ID / key
    userName TEXT NOT NULL,                            -- Login username
    passwordHash BLOB NOT NULL,                        -- Hashed password (bytes in python)
    creationTime datetime NOT NULL                     -- Time user was created
);
INSERT INTO "user" VALUES(3,'newUser','4d21e8140b3d294d4ca4e08accfb9c6aa7e4499face8b6e17b21f77ffc0a4a1d44282ce146fa12221c2244b9b1124612405b4ee0bab38e3c4bb5908399f6e36214d3749ce658dbecf5f81e2d2dc5a2fc8eaf557caaf67de2fb7471810d5dc21a','2022-04-24');
INSERT INTO "user" VALUES(4,'user','350966cb926c4675749ce05a07916f6a0b4f68623640cf4199fdc41aa2970d4527c11559d6c0e3f7671e4b3bad8bba14618a109829b0b4b2988d0cb8bc09199732a51bf2e6bd0e8d731259843f5bd3686930f14cfc4ed916dcd5d8373074de5a','2022-04-24');
COMMIT;
